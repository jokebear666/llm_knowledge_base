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
    """导出人工抽检清单：CSV（便于打开标注）+ JSON（便于回灌）。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "review_sheet.csv"
    json_path = out_dir / "review_questions.json"

    fields = ["id", "type", "category", "difficulty", "question", "answer", "tags", "source_doc", "reviewed_OK(1/0)"]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        for q in questions:
            writer.writerow([
                q.id, q.type.value, q.category, q.difficulty.value,
                q.question, q.answer, "/".join(q.tags), q.source_doc, "",
            ])

    json_path.write_text(
        json.dumps([q.model_dump(mode="json") for q in questions], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"质检清单已导出：\n  CSV(人工标注): {csv_path}\n  JSON(回灌入库): {json_path}")
    return csv_path, json_path


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
