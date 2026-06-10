"""命令行入口：编排完整流水线。

子命令：
  init-db    执行建表 SQL（含 pgvector）
  export     从语雀导出 .md（--namespace 或 --local 本地包）
  parse      解析 data/raw 为题目 JSON（--no-llm 可纯规则）
  qc         去重 + 导出人工抽检清单
  load       质检通过的题目入库 Supabase
  run        一键串联 export -> parse -> qc（入库需人工确认后再 load）
"""
from __future__ import annotations

import argparse
from pathlib import Path

from .config import PARSED_DIR, QC_DIR, config
from .exporter import export_from_api, import_local_package
from .loader import apply_schema, load_to_supabase
from .parser import load_questions, parse_all
from .qc import run_qc

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "sql" / "schema.sql"


def cmd_init_db(args):
    apply_schema(SCHEMA_PATH)


def cmd_export(args):
    config.ensure_dirs()
    if args.local:
        import_local_package(args.local)
    else:
        export_from_api(namespace=args.namespace)


def cmd_parse(args):
    config.ensure_dirs()
    parse_all(
        use_llm=not args.no_llm,
        concurrency=args.concurrency,
        resume=not args.no_resume,
    )


def cmd_qc(args):
    config.ensure_dirs()
    questions = load_questions(args.input)
    kept, embeddings = run_qc(questions, use_semantic=not args.no_semantic, threshold=args.threshold)
    # 落地去重后的题目与 embedding 供 load 复用
    from .parser import _dump
    _dump(kept, QC_DIR / "deduped_questions.json")
    import json
    (QC_DIR / "embeddings.json").write_text(json.dumps(embeddings), encoding="utf-8")


def cmd_load(args):
    questions = load_questions(args.input)
    embeddings = None
    emb_file = Path(args.embeddings) if args.embeddings else QC_DIR / "embeddings.json"
    if emb_file.exists():
        import json
        embeddings = json.loads(emb_file.read_text(encoding="utf-8"))
        if len(embeddings) != len(questions):
            embeddings = None
    load_to_supabase(questions, embeddings=embeddings, reviewed=not args.unreviewed)


def cmd_run(args):
    config.ensure_dirs()
    if args.local:
        import_local_package(args.local)
    elif args.namespace or config.yuque_namespace:
        export_from_api(namespace=args.namespace)
    else:
        print("跳过导出（未提供 --namespace / --local），直接使用 data/raw 现有文档。")

    questions = parse_all(use_llm=not args.no_llm, concurrency=args.concurrency)
    if not questions:
        return
    kept, embeddings = run_qc(questions, use_semantic=not args.no_semantic)

    from .parser import _dump
    import json
    _dump(kept, QC_DIR / "deduped_questions.json")
    (QC_DIR / "embeddings.json").write_text(json.dumps(embeddings), encoding="utf-8")

    print(
        "\n下一步（人工质检后再入库）：\n"
        f"  1) 打开并核对 {QC_DIR / 'review_sheet.csv'}\n"
        f"  2) 确认无误后入库：python -m quiz_pipeline.cli load "
        f"-i {QC_DIR / 'deduped_questions.json'}"
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="quiz_pipeline", description="语雀知识库 -> 结构化题库 流水线")
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("init-db", help="执行建表 SQL")
    sp.set_defaults(func=cmd_init_db)

    sp = sub.add_parser("export", help="从语雀导出 .md")
    sp.add_argument("--namespace", help="语雀知识库 namespace（默认读 .env）")
    sp.add_argument("--local", help="本地语雀 Markdown 导出包目录")
    sp.set_defaults(func=cmd_export)

    sp = sub.add_parser("parse", help="解析为题目 JSON")
    sp.add_argument("--no-llm", action="store_true", help="仅用规则解析，不调用 LLM")
    sp.add_argument("--concurrency", type=int, default=4, help="LLM 抽取并发度（默认 4）")
    sp.add_argument("--no-resume", action="store_true", help="不使用断点续跑缓存，全量重跑")
    sp.set_defaults(func=cmd_parse)

    sp = sub.add_parser("qc", help="去重 + 导出人工抽检清单")
    sp.add_argument("-i", "--input", default=str(PARSED_DIR / "questions.json"))
    sp.add_argument("--no-semantic", action="store_true", help="跳过 embedding 语义去重")
    sp.add_argument("--threshold", type=float, default=None, help="语义去重相似度阈值")
    sp.set_defaults(func=cmd_qc)

    sp = sub.add_parser("load", help="入库 Supabase")
    sp.add_argument("-i", "--input", default=str(QC_DIR / "deduped_questions.json"))
    sp.add_argument("-e", "--embeddings", default=None, help="embeddings.json 路径")
    sp.add_argument("--unreviewed", action="store_true", help="标记为未质检（默认已质检）")
    sp.set_defaults(func=cmd_load)

    sp = sub.add_parser("run", help="一键 export -> parse -> qc")
    sp.add_argument("--namespace")
    sp.add_argument("--local")
    sp.add_argument("--no-llm", action="store_true")
    sp.add_argument("--no-semantic", action="store_true")
    sp.add_argument("--concurrency", type=int, default=4, help="LLM 抽取并发度（默认 4）")
    sp.set_defaults(func=cmd_run)

    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
