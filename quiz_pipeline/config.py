"""集中读取环境变量配置。"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"          # 导出的原始 .md
PARSED_DIR = DATA_DIR / "parsed"   # 解析出的题目 JSON
QC_DIR = DATA_DIR / "qc"           # 质检产物


def _get(name: str, default: str | None = None) -> str | None:
    val = os.getenv(name)
    return val if val not in (None, "") else default


@dataclass
class Config:
    # 语雀
    yuque_token: str | None = _get("YUQUE_TOKEN")
    yuque_base_url: str = _get("YUQUE_BASE_URL", "https://www.yuque.com/api/v2")
    yuque_namespace: str | None = _get("YUQUE_NAMESPACE")

    # LLM（参考 llm_client.py 的 AzureGPTClient）
    gpt_ak: str | None = _get("GPT_AK") or _get("OPENAI_API_KEY")
    azure_endpoint: str = _get(
        "AZURE_OPENAI_ENDPOINT",
        "https://gpt-i18n.byteintl.net/gpt/openapi/online/responses",
    )
    azure_api_version: str = _get("AZURE_OPENAI_API_VERSION", "2024-03-01-preview")
    llm_model: str = _get("LLM_MODEL", "gpt-5.4-2026-03-05")  # deployment_name
    # 开源本地 embedding 模型（sentence-transformers）
    embedding_model: str = _get("EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5")
    embedding_dim: int = int(_get("EMBEDDING_DIM", "512"))  # 需与建表 vector(N) 一致

    # Supabase
    supabase_db_url: str | None = _get("SUPABASE_DB_URL")

    # 去重
    dedup_threshold: float = float(_get("DEDUP_SIMILARITY_THRESHOLD", "0.92"))

    def ensure_dirs(self) -> None:
        for d in (RAW_DIR, PARSED_DIR, QC_DIR):
            d.mkdir(parents=True, exist_ok=True)


config = Config()
