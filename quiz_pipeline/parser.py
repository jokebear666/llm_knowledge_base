"""第二步：解析为结构化题目（核心，方案 4.2）。

策略：规则解析 + LLM 抽取结合。
- 对格式规整的块（命中问答标记）优先用正则切分，成本低、可控。
- 其余块交给 LLM 强制 JSON 抽取/生成。
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable, Optional

from tqdm import tqdm

from .chunker import Chunk, chunk_markdown
from .config import PARSED_DIR
from .exporter import iter_raw_docs
from .llm import LLMClient
from .models import Question

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


def parse_document(
    name: str,
    body: str,
    llm: Optional[LLMClient] = None,
    use_llm: bool = True,
) -> list[Question]:
    """解析单篇文档为题目列表。"""
    questions: list[Question] = []
    for chunk in chunk_markdown(body):
        ruled = rule_parse_chunk(chunk, name)
        if ruled:
            questions.extend(ruled)
            continue
        if use_llm and llm is not None:
            questions.extend(llm_parse_chunk(chunk, name, llm))
    return questions


def parse_all(
    use_llm: bool = True,
    out_path: Path = PARSED_DIR / "questions.json",
) -> list[Question]:
    """解析 data/raw 下全部文档，落地 JSON。"""
    llm = LLMClient() if use_llm else None
    all_q: list[Question] = []
    docs = list(iter_raw_docs())
    if not docs:
        print("data/raw 下没有 .md，请先执行导出。")
        return []

    for name, body in tqdm(docs, desc="解析文档"):
        all_q.extend(parse_document(name, body, llm=llm, use_llm=use_llm))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    _dump(all_q, out_path)
    print(f"解析完成：{len(all_q)} 道题 -> {out_path}")
    return all_q


def _dump(questions: Iterable[Question], path: Path) -> None:
    data = [q.model_dump(mode="json") for q in questions]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_questions(path: Path) -> list[Question]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return [Question(**d).with_id() for d in data]
