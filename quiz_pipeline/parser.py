"""第二步：解析为结构化题目（核心，方案 4.2）。

策略：规则解析 + LLM 抽取结合。
- 对格式规整的块（命中问答标记）优先用正则切分，成本低、可控。
- 其余块交给 LLM 强制 JSON 抽取/生成。
"""
from __future__ import annotations

import hashlib
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, Optional

from tqdm import tqdm

from .chunker import Chunk, chunk_markdown
from .config import PARSED_DIR
from .exporter import iter_raw_docs
from .llm import LLMClient
from .models import Question

# 断点续跑缓存：记录每个 LLM 块的抽取结果（按块指纹），重跑时跳过已完成块
CACHE_PATH = PARSED_DIR / ".llm_cache.json"

# 规则解析：识别「Q: / 问: / 答案: / A:」一类显式问答标记
Q_MARK = re.compile(r"^\s*(?:Q[:：.]|问[:：.]|题目?[:：.])\s*", re.IGNORECASE)
A_MARK = re.compile(r"^\s*(?:A[:：.]|答[:：.]|答案[:：.]|参考答案[:：.])\s*", re.IGNORECASE)
HEADING_LINE = re.compile(r"^#{1,6}\s+(.+)$")


def _category_from_heading(heading: str) -> str:
    if not heading:
        return "未分类"
    return heading.split(" / ")[0].strip() or "未分类"


def rule_parse_chunk(chunk: Chunk, source_doc: str) -> list[Question]:
    """对显式问答结构的块做正则切分。返回空列表代表规则不适用。"""
    lines = chunk.text.splitlines()
    category = _category_from_heading(chunk.heading)

    questions: list[Question] = []
    cur_q: Optional[str] = None
    cur_a: list[str] = []
    mode = None  # "q" | "a"

    def flush():
        nonlocal cur_q, cur_a, mode
        if cur_q and cur_a:
            q = Question(
                question=cur_q,
                answer="\n".join(cur_a).strip(),
                category=category,
                tags=[t for t in chunk.heading.split(" / ") if t][1:],
                source_doc=source_doc,
            )
            if q.is_valid():
                questions.append(q.with_id())
        cur_q, cur_a, mode = None, [], None

    has_marker = False
    for line in lines:
        if Q_MARK.match(line):
            has_marker = True
            flush()
            cur_q = Q_MARK.sub("", line).strip()
            mode = "q"
        elif A_MARK.match(line):
            has_marker = True
            cur_a = [A_MARK.sub("", line).strip()]
            mode = "a"
        elif mode == "a":
            cur_a.append(line)
        elif mode == "q" and line.strip():
            cur_q = f"{cur_q} {line.strip()}".strip()
    flush()

    return questions if has_marker else []


def llm_parse_chunk(chunk: Chunk, source_doc: str, llm: LLMClient) -> list[Question]:
    """对散文式块用 LLM 抽取/生成。"""
    raw_items = llm.extract_questions(chunk.text, chunk.heading, source_doc)
    return _items_to_questions(raw_items, chunk, source_doc)


def parse_document(
    name: str,
    body: str,
    llm: Optional[LLMClient] = None,
    use_llm: bool = True,
) -> list[Question]:
    """解析单篇文档为题目列表（串行，供单篇/测试使用）。"""
    questions: list[Question] = []
    for chunk in chunk_markdown(body):
        ruled = rule_parse_chunk(chunk, name)
        if ruled:
            questions.extend(ruled)
            continue
        if use_llm and llm is not None:
            questions.extend(llm_parse_chunk(chunk, name, llm))
    return questions


def _chunk_fingerprint(name: str, chunk: Chunk) -> str:
    """块指纹：用于断点续跑缓存 key。"""
    raw = f"{name}\x00{chunk.heading}\x00{chunk.text}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()


def _load_cache() -> dict[str, list[dict]]:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def parse_all(
    use_llm: bool = True,
    out_path: Path = PARSED_DIR / "questions.json",
    concurrency: int = 4,
    resume: bool = True,
) -> list[Question]:
    """解析 data/raw 下全部文档，落地 JSON。

    - 规则命中的块即时处理（不耗 LLM）。
    - 散文块用线程池并发抽取（默认并发度 4）。
    - 断点续跑：已成功的块按指纹缓存，重跑时跳过。
    """
    docs = list(iter_raw_docs())
    if not docs:
        print("data/raw 下没有 .md，请先执行导出。")
        return []

    out_path.parent.mkdir(parents=True, exist_ok=True)

    all_q: list[Question] = []
    llm_tasks: list[tuple[str, Chunk]] = []  # (source_doc, chunk) 待 LLM 处理

    # 1) 先做规则解析，收集需要 LLM 的块
    for name, body in docs:
        for chunk in chunk_markdown(body):
            ruled = rule_parse_chunk(chunk, name)
            if ruled:
                all_q.extend(ruled)
            elif use_llm:
                llm_tasks.append((name, chunk))

    print(f"规则解析得到 {len(all_q)} 道题；待 LLM 抽取的块：{len(llm_tasks)}")
    if not use_llm or not llm_tasks:
        _dump(all_q, out_path)
        print(f"解析完成：{len(all_q)} 道题 -> {out_path}")
        return all_q

    # 2) 断点续跑：跳过缓存中已完成的块
    cache = _load_cache() if resume else {}
    cache_lock = threading.Lock()
    llm = LLMClient()

    pending: list[tuple[str, Chunk, str]] = []
    for name, chunk in llm_tasks:
        fp = _chunk_fingerprint(name, chunk)
        if fp in cache:
            all_q.extend(_items_to_questions(cache[fp], chunk, name))
        else:
            pending.append((name, chunk, fp))
    if len(pending) < len(llm_tasks):
        print(f"断点续跑：命中缓存 {len(llm_tasks) - len(pending)} 块，剩余 {len(pending)} 块需调用 LLM")

    # 3) 线程池并发抽取
    def _work(task: tuple[str, Chunk, str]) -> tuple[str, list[dict]]:
        name, chunk, fp = task
        raw_items = llm.extract_questions(chunk.text, chunk.heading, name)
        return fp, raw_items

    failed = 0
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(_work, t): t for t in pending}
        for fut in tqdm(as_completed(futures), total=len(futures), desc=f"LLM抽取(并发{concurrency})"):
            name, chunk, fp = futures[fut]
            try:
                fp, raw_items = fut.result()
            except Exception as e:
                failed += 1
                tqdm.write(f"  [失败] {name} / {chunk.heading[:40]}: {e}")
                continue
            with cache_lock:
                cache[fp] = raw_items
                CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            all_q.extend(_items_to_questions(raw_items, chunk, name))

    if failed:
        print(f"⚠ {failed} 个块抽取失败（已重试），可重新运行 parse 续跑这些块。")

    _dump(all_q, out_path)
    print(f"解析完成：{len(all_q)} 道题 -> {out_path}")
    return all_q


def _items_to_questions(raw_items: list[dict], chunk: Chunk, source_doc: str) -> list[Question]:
    """把 LLM 原始 items 转成 Question（与 llm_parse_chunk 同逻辑，供缓存复用）。"""
    out: list[Question] = []
    fallback_cat = _category_from_heading(chunk.heading)
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        item.setdefault("category", fallback_cat)
        item["source_doc"] = source_doc
        try:
            q = Question(**item)
        except Exception:
            continue
        if q.is_valid():
            out.append(q.with_id())
    return out


def _dump(questions: Iterable[Question], path: Path) -> None:
    data = [q.model_dump(mode="json") for q in questions]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_questions(path: Path) -> list[Question]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Question(**d).with_id() for d in data]
