"""统一题目数据结构（对应方案 4.1）。"""
from __future__ import annotations

import hashlib
import re
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class QuestionType(str, Enum):
    BAGU = "八股"
    MIANJING = "面经"
    ALGORITHM = "算法"


class Difficulty(str, Enum):
    EASY = "易"
    MEDIUM = "中"
    HARD = "难"


class QuestionKind(str, Enum):
    """题目的提问角度类型（按题干句式判定）。"""

    COMPARE = "区别对比类"
    PRINCIPLE = "原理机制类"
    PURPOSE = "作用目的类"
    WHY = "动机原因类"
    SCENARIO = "场景适用类"
    METHOD = "方法实践类"
    DEFINITION = "定义概念类"
    TRADEOFF = "优缺点取舍类"
    CLASSIFY = "分类构成类"
    PROCEDURE = "步骤流程类"
    OTHER = "其他"


class InterviewFit(str, Enum):
    """面试适合度：该提问类型在真实面试中出现的概率。"""

    HIGH = "高频"
    MEDIUM = "中频"
    LOW = "低频"
    INVALID = "无效"


class ChoiceKind(str, Enum):
    """选择题类型：单选 / 多选。"""

    SINGLE = "单选"
    MULTIPLE = "多选"


# 提问类型 -> 面试适合度 映射（依据面试官出题动机分析）
QUESTION_KIND_TO_FIT: dict[QuestionKind, InterviewFit] = {
    QuestionKind.COMPARE: InterviewFit.HIGH,
    QuestionKind.WHY: InterviewFit.HIGH,
    QuestionKind.TRADEOFF: InterviewFit.HIGH,
    QuestionKind.PRINCIPLE: InterviewFit.HIGH,
    QuestionKind.SCENARIO: InterviewFit.MEDIUM,
    QuestionKind.METHOD: InterviewFit.MEDIUM,
    QuestionKind.DEFINITION: InterviewFit.MEDIUM,
    QuestionKind.PURPOSE: InterviewFit.LOW,
    QuestionKind.CLASSIFY: InterviewFit.LOW,
    QuestionKind.PROCEDURE: InterviewFit.LOW,
    QuestionKind.OTHER: InterviewFit.INVALID,
}


def interview_fit_of(kind: QuestionKind) -> InterviewFit:
    return QUESTION_KIND_TO_FIT.get(kind, InterviewFit.INVALID)


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
    question_kind: QuestionKind = QuestionKind.OTHER  # 提问角度类型
    interview_fit: InterviewFit = InterviewFit.INVALID  # 面试适合度（由 question_kind 推导）
    source_doc: str = ""

    # ===== 选择题（由 to-choice 步骤生成；未生成时为空，仍可作开放问答）=====
    choice_kind: Optional[ChoiceKind] = None       # 单选 / 多选
    options: List[str] = Field(default_factory=list)  # 选项文本（已打乱顺序）
    correct_index: List[int] = Field(default_factory=list)  # 正确选项下标（单选长度1，多选>=2）

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

    @model_validator(mode="after")
    def _derive_interview_fit(self):
        """面试适合度始终由 question_kind 推导，保持一致。"""
        self.interview_fit = interview_fit_of(self.question_kind)
        return self

    def fingerprint(self) -> str:
        """基于题干生成的稳定指纹，用作 id 与精确去重 key。"""
        return hashlib.sha1(_slug(self.question).encode("utf-8")).hexdigest()[:16]

    def with_id(self) -> "Question":
        if not self.id:
            self.id = self.fingerprint()
        return self

    def is_valid(self) -> bool:
        return bool(self.question) and bool(self.answer)

    def has_choice(self) -> bool:
        """是否已生成合法的选择题（选项数>=2 且正确项下标合法）。"""
        if self.choice_kind is None or len(self.options) < 2 or not self.correct_index:
            return False
        n = len(self.options)
        if any(i < 0 or i >= n for i in self.correct_index):
            return False
        if self.choice_kind == ChoiceKind.SINGLE and len(self.correct_index) != 1:
            return False
        if self.choice_kind == ChoiceKind.MULTIPLE and len(self.correct_index) < 2:
            return False
        return True
