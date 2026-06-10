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

# ===== 硬规则一票否决：命中即淘汰，不再送 LLM 打分（省成本）=====
# 题干命中即淘汰（时间/背景/为什么火 等开放发散与元信息类）
_HARD_Q_PATTERNS = [
    r"提出背景|出现背景|诞生背景|历史背景",
    r"什么时候|何时(确立|提出|诞生|出现|规范)|哪一年|发展历程|发展史|演进历程|演变历程|时间线",
    r"为(什么|何)(会)?(火|流行|爆火|出圈|受欢迎|成为热点|走红)",
    r"由谁(提出|命名|发明|创造)|是谁(提出|命名|发明|创造)|谁(提出|命名|发明|创造|首次提出)了",
    r"哪(个|家)(机构|公司|组织|团队)(提出|发布|命名)",
    r"(术语|概念|名词)(是)?(何时|什么时候|由谁)(规范|命名|提出|确立)",
    r"(意义|价值|影响|前景|展望|趋势)(是什么|有哪些|如何)?$",
]
# 题干/答案命中即淘汰（人物言论/观点理念类）
_HARD_PERSON_VIEW = [
    r"(的(观点|理念|主张|看法|分类|定义))(是什么|有哪些)",
    r"(如何|怎样|怎么)(看待|评价|理解)\s*[\u4e00-\u9fffA-Za-z]+(的)",
]
# 答案命中即淘汰（指代外部语境，破坏自包含性）
_HARD_A_PATTERNS = [
    r"本文|该文|该报告|本报告|本节|本章|上文|前文|如前所述|上(面|述)(提到|所说)|如(上|下)(图|表|所示)|文中(提到|指出|所说)",
]

_HARD_Q_RE = re.compile("|".join(_HARD_Q_PATTERNS))
_HARD_PV_RE = re.compile("|".join(_HARD_PERSON_VIEW))
_HARD_A_RE = re.compile("|".join(_HARD_A_PATTERNS))


def hard_reject(item: dict) -> Optional[str]:
    """硬规则一票否决：命中返回淘汰原因，未命中返回 None。"""
    q = (item.get("question") or "").strip()
    a = (item.get("answer") or "").strip()
    if _HARD_Q_RE.search(q):
        return "硬规则:时间/背景/为何火/元信息类题干"
    if _HARD_PV_RE.search(q) or _HARD_PV_RE.search(a):
        return "硬规则:人物言论/观点理念类"
    if _HARD_A_RE.search(a):
        return "硬规则:答案指代外部语境(破坏自包含性)"
    return None


def hard_filter(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """对一组题先过硬规则，返回 (通过, 被淘汰)。被淘汰项带 _drop_reason。"""
    passed, rejected = [], []
    for it in items:
        reason = hard_reject(it)
        if reason:
            it = dict(it)
            it["_drop_reason"] = reason
            rejected.append(it)
        else:
            passed.append(it)
    return passed, rejected

# 规则解析：识别「Q: / 问: / 答案: / A:」一类显式问答标记
Q_MARK = re.compile(r"^\s*(?:Q[:：.]|问[:：.]|题目?[:：.])\s*", re.IGNORECASE)
A_MARK = re.compile(r"^\s*(?:A[:：.]|答[:：.]|答案[:：.]|参考答案[:：.])\s*", re.IGNORECASE)
HEADING_LINE = re.compile(r"^#{1,6}\s+(.+)$")


# 圈数字/带圈序号等装饰性前缀（语雀标题常见，如 ① ⓵ ② ➀ 1. 一、）
_SEQ_PREFIX = re.compile(
    r"^[\s\u2460-\u24ff\u2776-\u2793\u3220-\u3229\u3251-\u325f\u32b1-\u32bf"
    r"0-9①-⑳⓪-⓿\.\)、\-—_]+"
)


def _clean_category(title: str) -> str:
    """清洗分类名：去圈数字/序号前缀、归一空格。"""
    t = title.replace("_", " ")
    t = _SEQ_PREFIX.sub("", t)        # 去掉开头的序号/圈数字/标点
    t = re.sub(r"\s+", " ", t).strip()
    return t or title.strip() or "未分类"


def _category_from_source(source_doc: str) -> str:
    """从来源文件名推导稳定的「知识领域」分类。

    导出文件名形如「4__语音大模型__go342l3xnxz302iv.md」，取中间的文档标题作 category，
    这是稳定的学科领域（便于跨文档检索与薄弱点推荐），小节标题则降级进 tags。
    标题里的圈数字/序号前缀会被清洗掉，避免「① xxx」这类脏分类。
    """
    stem = source_doc.rsplit(".", 1)[0]  # 去扩展名
    parts = stem.split("__")
    # 形如 [序号, 标题, slug]；取标题段。兼容无序号 (前缀为空) 的情况。
    if len(parts) >= 3:
        title = parts[1].strip()
    elif len(parts) == 2:
        title = parts[0].strip() or parts[1].strip()
    else:
        title = stem.strip()
    return _clean_category(title)


def _heading_tags(heading: str) -> list[str]:
    """把小节标题路径拆成 tags（去掉空段）。"""
    return [t.strip() for t in heading.split(" / ") if t.strip()]


def rule_parse_chunk(chunk: Chunk, source_doc: str) -> list[Question]:
    """对显式问答结构的块做正则切分。返回空列表代表规则不适用。"""
    lines = chunk.text.splitlines()
    category = _category_from_source(source_doc)
    heading_tags = _heading_tags(chunk.heading)

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
                tags=heading_tags,
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


def llm_parse_chunk(chunk: Chunk, source_doc: str, llm: LLMClient, reflect: bool = True) -> list[Question]:
    """对散文式块用 LLM 抽取/生成：抽取 → 硬规则一票否决 →（可选）反思过滤。"""
    raw_items = llm.extract_questions(chunk.text, chunk.heading, source_doc)
    raw_items, _ = hard_filter(raw_items)
    if reflect and raw_items:
        raw_items, _ = llm.reflect_filter(raw_items)
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
    reflect: bool = True,
) -> list[Question]:
    """解析 data/raw 下全部文档，落地 JSON。

    - 规则命中的块即时处理（不耗 LLM）。
    - 散文块用线程池并发抽取（默认并发度 4）。
    - reflect=True 时，每块抽取后追加一次 LLM 反思过滤，剔除不合理题目。
    - 断点续跑：已成功的块按指纹缓存（缓存的是反思后的结果），重跑时跳过。
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

    # 3) 线程池并发：抽取 → 硬规则一票否决 →（可选）LLM 反思打分。缓存的是最终保留的题目。
    def _work(task: tuple[str, Chunk, str]) -> tuple[str, list[dict], int, int]:
        name, chunk, fp = task
        raw_items = llm.extract_questions(chunk.text, chunk.heading, name)
        # 3a) 硬规则：命中即淘汰，不送 LLM 打分（省成本）
        raw_items, hard_rejected = hard_filter(raw_items)
        hard_n = len(hard_rejected)
        # 3b) LLM 反思打分（仅对通过硬规则的题）
        reflect_n = 0
        if reflect and raw_items:
            kept, dropped = llm.reflect_filter(raw_items)
            reflect_n = len(dropped)
            raw_items = kept
        return fp, raw_items, hard_n, reflect_n

    failed = 0
    total_hard = 0
    total_reflect = 0
    desc = f"LLM抽取+反思(并发{concurrency})" if reflect else f"LLM抽取(并发{concurrency})"
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(_work, t): t for t in pending}
        for fut in tqdm(as_completed(futures), total=len(futures), desc=desc):
            name, chunk, fp = futures[fut]
            try:
                fp, raw_items, hard_n, reflect_n = fut.result()
            except Exception as e:
                failed += 1
                tqdm.write(f"  [失败] {name} / {chunk.heading[:40]}: {e}")
                continue
            total_hard += hard_n
            total_reflect += reflect_n
            with cache_lock:
                cache[fp] = raw_items
                CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            all_q.extend(_items_to_questions(raw_items, chunk, name))

    print(f"硬规则一票否决：淘汰 {total_hard} 道")
    if reflect:
        print(f"反思过滤：剔除 {total_reflect} 道不合理题目")
    if failed:
        print(f"⚠ {failed} 个块抽取失败（已重试），可重新运行 parse 续跑这些块。")

    _dump(all_q, out_path)
    print(f"解析完成：{len(all_q)} 道题 -> {out_path}")
    return all_q


def _items_to_questions(raw_items: list[dict], chunk: Chunk, source_doc: str) -> list[Question]:
    """把 LLM 原始 items 转成 Question（与 llm_parse_chunk 同逻辑，供缓存复用）。

    category 统一由来源文档推导（稳定知识领域），小节标题并入 tags；
    忽略 LLM 可能输出的 category（prompt 已要求不输出）。
    """
    out: list[Question] = []
    category = _category_from_source(source_doc)
    heading_tags = _heading_tags(chunk.heading)
    for item in raw_items:
        if not isinstance(item, dict):
            continue
        item.pop("category", None)  # 由系统统一填，忽略模型输出
        item["category"] = category
        item["source_doc"] = source_doc
        # 合并：小节标题 tags + 模型 tags（去重保序）
        model_tags = item.get("tags") or []
        if isinstance(model_tags, str):
            model_tags = [model_tags]
        merged, seen = [], set()
        for t in [*heading_tags, *model_tags]:
            ts = str(t).strip()
            if ts and ts not in seen:
                seen.add(ts)
                merged.append(ts)
        item["tags"] = merged
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
