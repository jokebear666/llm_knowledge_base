"""第二步前置：长文档按小节切块（方案 4.3.1）。

按 Markdown 标题层级切分；过长的块再按字符数二次切分，
避免超长上下文导致 LLM 质量下降和成本飙升。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


@dataclass
class Chunk:
    heading: str   # 该块所属标题路径，如 "操作系统 / 进程与线程"
    text: str      # 块正文（含标题）


def _split_long(text: str, max_chars: int) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    paras = text.split("\n\n")
    out, buf = [], ""
    for p in paras:
        if len(buf) + len(p) + 2 > max_chars and buf:
            out.append(buf)
            buf = p
        else:
            buf = f"{buf}\n\n{p}" if buf else p
    if buf:
        out.append(buf)
    return out


def chunk_markdown(md: str, max_chars: int = 4000, min_chars: int = 40) -> list[Chunk]:
    """把一篇 Markdown 切成若干语义块。"""
    matches = list(HEADING_RE.finditer(md))
    if not matches:
        return [Chunk("", part) for part in _split_long(md.strip(), max_chars) if len(part.strip()) >= min_chars]

    chunks: list[Chunk] = []
    stack: list[tuple[int, str]] = []  # (level, title) 维护标题路径

    for i, m in enumerate(matches):
        level = len(m.group(1))
        title = m.group(2).strip()
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        body = md[start:end].strip()

        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, title))
        heading_path = " / ".join(t for _, t in stack)

        if len(body) < min_chars:
            continue
        for part in _split_long(body, max_chars):
            chunks.append(Chunk(heading_path, part))
    return chunks
