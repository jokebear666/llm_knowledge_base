"""第三步：人工质检 + 去重（方案五）。

- 精确去重：按题干指纹。
- 语义去重：按题干 embedding 余弦相似度，超阈值判为重复。
- 导出人工抽检清单（CSV + JSON），人工标注 reviewed 后再入库。
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Optional

import numpy as np
from tqdm import tqdm

from .config import QC_DIR, config
from .llm import LLMClient
from .models import Question


def dedup_exact(questions: list[Question]) -> list[Question]:
    """按题干指纹精确去重。"""
    seen: set[str] = set()
    out: list[Question] = []
    for q in questions:
        fp = q.fingerprint()
        if fp in seen:
            continue
        seen.add(fp)
        out.append(q.with_id())
    return out


def _cosine_matrix(vecs: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(vecs, axis=1, keepdims=True)
    norms[norms == 0] = 1e-9
    unit = vecs / norms
    return unit @ unit.T


def dedup_semantic(
    questions: list[Question],
    embeddings: list[list[float]],
    threshold: Optional[float] = None,
) -> tuple[list[Question], list[tuple[str, str, float]]]:
    """按题干 embedding 相似度去重。

    返回 (保留的题目, 被判重对 [(保留id, 丢弃id, 相似度)])。
    """
    threshold = threshold if threshold is not None else config.dedup_threshold
    if not questions:
        return [], []

    vecs = np.array(embeddings, dtype=np.float32)
    sim = _cosine_matrix(vecs)

    keep_idx: list[int] = []
    dropped: list[tuple[str, str, float]] = []
    removed = set()

    for i in range(len(questions)):
        if i in removed:
            continue
        keep_idx.append(i)
        for j in range(i + 1, len(questions)):
            if j in removed:
                continue
            if sim[i, j] >= threshold:
                removed.add(j)
                dropped.append((questions[i].id, questions[j].id, float(sim[i, j])))

    return [questions[i] for i in keep_idx], dropped


def embed_questions(questions: list[Question], llm: LLMClient, batch: int = 64) -> list[list[float]]:
    """批量为题干生成 embedding。"""
    embeddings: list[list[float]] = []
    for i in tqdm(range(0, len(questions), batch), desc="生成 embedding"):
        chunk = [q.question for q in questions[i : i + batch]]
        embeddings.extend(llm.embed(chunk))
    return embeddings


def export_review_sheet(questions: list[Question], out_dir: Path = QC_DIR) -> tuple[Path, Path]:
    """导出人工抽检清单：TSV（便于打开标注）+ JSON（便于回灌）。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    tsv_path = out_dir / "review_sheet.tsv"
    json_path = out_dir / "review_questions.json"

    fields = [
        "id", "type", "category", "difficulty", "question_kind", "interview_fit",
        "question", "answer", "tags", "source_doc", "reviewed_OK(1/0)",
    ]

    def _clean(s: str) -> str:
        # TSV 以制表符分隔、换行分行，单元格内的 \t \r \n 需替换避免错位
        return (s or "").replace("\t", " ").replace("\r", " ").replace("\n", " ")

    with tsv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(fields)
        for q in questions:
            writer.writerow([
                q.id, q.type.value, q.category, q.difficulty.value,
                q.question_kind.value, q.interview_fit.value,
                _clean(q.question), _clean(q.answer), "/".join(q.tags), q.source_doc, "",
            ])

    json_path.write_text(
        json.dumps([q.model_dump(mode="json") for q in questions], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"质检清单已导出：\n  TSV(人工标注): {tsv_path}\n  JSON(回灌入库): {json_path}")
    return tsv_path, json_path


def apply_review(
    tsv_path: Path = QC_DIR / "review_sheet.tsv",
    out_path: Path = QC_DIR / "reviewed_questions_final.json",
) -> list[Question]:
    """读取人工标注的 TSV，回灌标注结果，产出最终入库源。

    规则：
    - reviewed_OK 列填 1/通过/ok/yes/true 视为保留；填 0/x 视为淘汰；留空默认保留（视为未发现问题）。
    - 采纳人工在 TSV 中对 question/answer/difficulty/category/tags 的修改。
    - id 以题干为指纹，人工改了题干会重算 id。
    """
    if not tsv_path.exists():
        raise FileNotFoundError(f"未找到标注文件：{tsv_path}，请先运行 qc 生成并人工标注。")

    keep_tokens = {"1", "通过", "ok", "yes", "y", "true", "保留", "对", "√", "✓"}
    drop_tokens = {"0", "淘汰", "no", "n", "false", "x", "×", "错", "删除"}

    kept: list[Question] = []
    n_total = n_drop = n_blank = 0
    with tsv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            n_total += 1
            mark = (row.get("reviewed_OK(1/0)") or "").strip().lower()
            if mark in drop_tokens:
                n_drop += 1
                continue
            if mark == "":
                n_blank += 1  # 留空默认保留
            elif mark not in keep_tokens:
                # 未识别的标记，保守保留并提示
                n_blank += 1

            tags_raw = (row.get("tags") or "").strip()
            tags = [t for t in tags_raw.split("/") if t.strip()] if tags_raw else []
            data = {
                "type": (row.get("type") or "八股").strip() or "八股",
                "question": (row.get("question") or "").strip(),
                "answer": (row.get("answer") or "").strip(),
                "category": (row.get("category") or "未分类").strip() or "未分类",
                "tags": tags,
                "difficulty": (row.get("difficulty") or "中").strip() or "中",
                "question_kind": (row.get("question_kind") or "其他").strip() or "其他",
                "source_doc": (row.get("source_doc") or "").strip(),
            }
            try:
                q = Question(**data)
            except Exception:
                continue
            if q.is_valid():
                kept.append(q.with_id())

    out_path.write_text(
        json.dumps([q.model_dump(mode="json") for q in kept], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"标注回灌完成：共 {n_total} 题，淘汰 {n_drop} 题，保留 {len(kept)} 题"
        f"（其中 {n_blank} 题未明确标注按保留处理）\n  -> {out_path}"
    )
    return kept


def run_qc(
    questions: list[Question],
    use_semantic: bool = True,
    threshold: Optional[float] = None,
) -> tuple[list[Question], list[list[float]]]:
    """执行精确 + 语义去重，导出抽检清单。返回 (题目, embeddings)。"""
    before = len(questions)
    questions = dedup_exact(questions)
    print(f"精确去重：{before} -> {len(questions)}")

    embeddings: list[list[float]] = []
    if use_semantic and questions:
        llm = LLMClient()
        embeddings = embed_questions(questions, llm)
        kept, dropped = dedup_semantic(questions, embeddings, threshold)
        # 同步裁剪 embeddings
        kept_ids = {q.id for q in kept}
        id_to_emb = {q.id: e for q, e in zip(questions, embeddings)}
        questions = kept
        embeddings = [id_to_emb[q.id] for q in questions]
        print(f"语义去重：移除 {len(dropped)} 道近似题 -> 剩余 {len(questions)}")
        if dropped:
            (QC_DIR).mkdir(parents=True, exist_ok=True)
            (QC_DIR / "dedup_report.json").write_text(
                json.dumps(
                    [{"kept": k, "dropped": d, "similarity": round(s, 4)} for k, d, s in dropped],
                    ensure_ascii=False, indent=2,
                ),
                encoding="utf-8",
            )

    export_review_sheet(questions)
    return questions, embeddings
