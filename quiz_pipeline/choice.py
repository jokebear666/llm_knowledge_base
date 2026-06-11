"""第五步：问答题 -> 选择题转换（放在 review 之后、load 之前）。

对每道题调用一次 LLM，判定单选/多选并生成选项（正确项 + 似是而非的干扰项）。
Python 侧负责打乱选项顺序、计算正确项下标，避免依赖 LLM 直接给下标。

特性（复用 parser 的工程化模式）：
- 线程池并发（默认 4）。
- 断点续跑：按题目 id 缓存已生成的选择题，重跑跳过。
- 重试：to_choice 内部指数退避。
"""
from __future__ import annotations

import json
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional

from tqdm import tqdm

from .config import QC_DIR
from .llm import LLMClient
from .models import ChoiceKind, Question
from .parser import _dump, load_questions

# 断点续跑缓存：按题目 id 记录已生成的选择题原始结果
CACHE_PATH = QC_DIR / ".choice_cache.json"


def _assemble_choice(result: dict, seed: str) -> Optional[dict]:
    """把 LLM 结果（correct/distractors）组装成打乱后的 options + correct_index。

    统一生成**单选题**：恰好 1 个正确项 + 3 个干扰项 = 4 个选项。
    即使 LLM 多给了正确项/干扰项也会被截断，保证选项数恒为 4。
    返回 {"choice_kind", "options", "correct_index"}；非法则 None。
    seed 用题目 id，保证同一题打乱结果稳定可复现。
    """
    correct = [c for c in (result.get("correct") or []) if c]
    distractors = [d for d in (result.get("distractors") or []) if d]
    if not correct or not distractors:
        return None

    # 去重，避免正确项与干扰项文本重复导致下标歧义
    seen = set()
    uniq_correct, uniq_distractors = [], []
    for c in correct:
        if c not in seen:
            seen.add(c)
            uniq_correct.append(c)
    for d in distractors:
        if d not in seen:
            seen.add(d)
            uniq_distractors.append(d)

    # 强制单选：恰好 1 正确项 + 3 干扰项
    uniq_correct = uniq_correct[:1]
    uniq_distractors = uniq_distractors[:3]
    if len(uniq_distractors) < 3:
        return None  # 干扰项不足，无法凑齐 4 选项，跳过（可重跑补齐）

    options = uniq_correct + uniq_distractors  # 恒为 4 个
    rng = random.Random(seed)
    order = list(range(len(options)))
    rng.shuffle(order)
    shuffled = [options[i] for i in order]
    correct_index = sorted(pos for pos, orig in enumerate(order) if orig == 0)

    return {
        "choice_kind": ChoiceKind.SINGLE,
        "options": shuffled,
        "correct_index": correct_index,
    }


def _load_cache() -> dict[str, dict]:
    if CACHE_PATH.exists():
        try:
            return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _apply_to_question(q: Question, assembled: dict) -> None:
    q.choice_kind = assembled["choice_kind"]
    q.options = assembled["options"]
    q.correct_index = assembled["correct_index"]


def to_choice_all(
    in_path: Path = QC_DIR / "reviewed_questions_final.json",
    out_path: Path = QC_DIR / "choice_questions.json",
    concurrency: int = 4,
    resume: bool = True,
) -> list[Question]:
    """对入库源里的全部题目生成选择题，落地 JSON。"""
    questions = load_questions(Path(in_path))
    if not questions:
        print(f"{in_path} 没有题目。")
        return []

    out_path.parent.mkdir(parents=True, exist_ok=True)
    cache = _load_cache() if resume else {}
    cache_lock = threading.Lock()
    llm = LLMClient()

    # 命中缓存直接应用，未命中的进待处理队列
    pending: list[Question] = []
    for q in questions:
        q.with_id()
        cached = cache.get(q.id)
        if cached:
            assembled = _assemble_choice(cached, seed=q.id)
            if assembled:
                _apply_to_question(q, assembled)
                continue
        pending.append(q)

    if len(pending) < len(questions):
        print(f"断点续跑：命中缓存 {len(questions) - len(pending)} 题，剩余 {len(pending)} 题需调用 LLM")

    def _work(q: Question) -> tuple[str, Optional[dict]]:
        result = llm.to_choice(q.question, q.answer)
        return q.id, result

    failed = 0
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = {pool.submit(_work, q): q for q in pending}
        for fut in tqdm(as_completed(futures), total=len(futures), desc=f"生成选择题(并发{concurrency})"):
            q = futures[fut]
            try:
                qid, result = fut.result()
            except Exception as e:
                failed += 1
                tqdm.write(f"  [失败] {q.question[:40]}: {e}")
                continue
            if not result:
                failed += 1
                continue
            with cache_lock:
                cache[qid] = result
                CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            assembled = _assemble_choice(result, seed=qid)
            if assembled:
                _apply_to_question(q, assembled)

    single = sum(1 for q in questions if q.choice_kind == ChoiceKind.SINGLE)
    multiple = sum(1 for q in questions if q.choice_kind == ChoiceKind.MULTIPLE)
    none_cnt = sum(1 for q in questions if not q.has_choice())
    print(f"选择题生成完成：单选 {single}，多选 {multiple}，未生成 {none_cnt}")
    if failed:
        print(f"⚠ {failed} 题生成失败（可重新运行 to-choice 续跑）。")

    _dump(questions, out_path)
    print(f"已落地：{len(questions)} 题 -> {out_path}")
    return questions
