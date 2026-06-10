"""统一题目数据结构（对应方案 4.1）。"""
from __future__ import annotations

import hashlib
import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class QuestionType(str, Enum):
    BAGU = "八股"
    MIANJING = "面经"
    ALGORITHM = "算法"


class Difficulty(str, Enum):
    EASY = "易"
    MEDIUM = "中"
    HARD = "难"


def _slug(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip().lower()


class Question(BaseModel):
    """一道结构化题目。"""

    id: Optional[str] = None
    type: QuestionType = QuestionType.BAGU
    question: str
    answer: str
    category: str = "未分类"
    tags: List[str] = Field(default_factory=list)
    difficulty: Difficulty = Difficulty.MEDIUM
    source_doc: str = ""

    @field_validator("tags", mode="before")
    @classmethod
    def _norm_tags(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            v = [t for t in re.split(r"[,，;；/]", v) if t.strip()]
        return [t.strip() for t in v if str(t).strip()]

    @field_validator("question", "answer", mode="before")
    @classmethod
    def _strip(cls, v):
        return (v or "").strip()

    def fingerprint(self) -> str:
        """基于题干生成的稳定指纹，用作 id 与精确去重 key。"""
        return hashlib.sha1(_slug(self.question).encode("utf-8")).hexdigest()[:16]

    def with_id(self) -> "Question":
        if not self.id:
            self.id = self.fingerprint()
        return self

    def is_valid(self) -> bool:
        return bool(self.question) and bool(self.answer)
