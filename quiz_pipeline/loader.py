"""第四步：入库 Supabase（PostgreSQL + pgvector）。

将质检通过的题目批量 upsert 进 questions 表，并写入题干 embedding。
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import psycopg2
from psycopg2.extras import execute_values
from tqdm import tqdm

from .config import config
from .llm import LLMClient
from .models import Question


def _vec_literal(embedding: Optional[list[float]]) -> Optional[str]:
    """转成 pgvector 字面量 '[a,b,c]'。"""
    if embedding is None:
        return None
    return "[" + ",".join(f"{x:.6f}" for x in embedding) + "]"


UPSERT_SQL = """
insert into questions
    (id, type, question, answer, category, tags, difficulty, source_doc, embedding, reviewed, updated_at)
values %s
on conflict (id) do update set
    type = excluded.type,
    question = excluded.question,
    answer = excluded.answer,
    category = excluded.category,
    tags = excluded.tags,
    difficulty = excluded.difficulty,
    source_doc = excluded.source_doc,
    embedding = coalesce(excluded.embedding, questions.embedding),
    reviewed = excluded.reviewed,
    updated_at = now();
"""


def load_to_supabase(
    questions: list[Question],
    embeddings: Optional[list[list[float]]] = None,
    reviewed: bool = True,
    backfill_embeddings: bool = True,
) -> int:
    """批量写入题库。embeddings 缺失时按需用 LLM 补齐。"""
    if not config.supabase_db_url:
        raise ValueError("缺少 SUPABASE_DB_URL，请在 .env 中配置。")
    if not questions:
        print("没有可入库的题目。")
        return 0

    emb_map: dict[str, list[float]] = {}
    if embeddings and len(embeddings) == len(questions):
        emb_map = {q.id: e for q, e in zip(questions, embeddings)}
    elif backfill_embeddings:
        llm = LLMClient()
        missing = [q for q in questions]
        print(f"为 {len(missing)} 道题补齐 embedding ...")
        for i in tqdm(range(0, len(missing), 64), desc="embedding"):
            chunk = missing[i : i + 64]
            vecs = llm.embed([q.question for q in chunk])
            for q, v in zip(chunk, vecs):
                emb_map[q.id] = v

    rows = []
    for q in questions:
        rows.append((
            q.with_id().id,
            q.type.value,
            q.question,
            q.answer,
            q.category,
            q.tags,
            q.difficulty.value,
            q.source_doc,
            _vec_literal(emb_map.get(q.id)),
            reviewed,
        ))

    conn = psycopg2.connect(config.supabase_db_url)
    try:
        with conn, conn.cursor() as cur:
            execute_values(
                cur,
                UPSERT_SQL,
                rows,
                template="(%s,%s,%s,%s,%s,%s,%s,%s,%s::vector,%s,now())",
                page_size=100,
            )
        print(f"入库完成：{len(rows)} 道题已 upsert 到 Supabase。")
        return len(rows)
    finally:
        conn.close()


def apply_schema(schema_path: Path) -> None:
    """执行建表 SQL（首次初始化用）。"""
    if not config.supabase_db_url:
        raise ValueError("缺少 SUPABASE_DB_URL。")
    sql = Path(schema_path).read_text(encoding="utf-8")
    conn = psycopg2.connect(config.supabase_db_url)
    try:
        with conn, conn.cursor() as cur:
            cur.execute(sql)
        print("建表 SQL 执行完成。")
    finally:
        conn.close()
