"""第一步：从语雀导出文档为本地 .md 集合（方案三）。

支持两种来源：
1. 语雀 OpenAPI：列出知识库目录 -> 逐篇拉正文（推荐，可重复执行）。
2. 本地 Markdown 导出包目录：直接归整已有 .md。
"""
from __future__ import annotations

import re
import shutil
import time
from pathlib import Path
from typing import Iterator

import requests
from tqdm import tqdm

from .config import RAW_DIR, config


def _safe_filename(title: str, slug: str) -> str:
    name = re.sub(r"[^\w\u4e00-\u9fff\- ]+", "_", title or slug or "untitled").strip()
    name = re.sub(r"\s+", "_", name)[:80]
    return f"{name}__{slug}.md"


class YuqueClient:
    """语雀 OpenAPI 轻封装。"""

    def __init__(self, token: str | None = None, base_url: str | None = None):
        self.token = token or config.yuque_token
        self.base_url = (base_url or config.yuque_base_url).rstrip("/")
        if not self.token:
            raise ValueError("缺少 YUQUE_TOKEN，请在 .env 中配置。")
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-Auth-Token": self.token,
                "User-Agent": "quiz-pipeline/0.1",
                "Content-Type": "application/json",
            }
        )

    def _get(self, path: str, **params) -> dict:
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("data", {})

    def list_docs(self, namespace: str, per_page: int = 100) -> list[dict]:
        """列出知识库下全部文档（自动翻页，确保全量）。

        语雀 /repos/{ns}/docs 默认每页约 100 条，超过则需翻页，
        否则大知识库会漏掉靠后的文档。
        """
        all_docs: list[dict] = []
        offset = 0
        while True:
            page = self._get(
                f"/repos/{namespace}/docs",
                offset=offset,
                limit=per_page,
            )
            if not page:
                break
            all_docs.extend(page)
            if len(page) < per_page:
                break
            offset += per_page
        return all_docs

    def get_doc(self, namespace: str, slug: str) -> dict:
        """拉取单篇文档正文（Markdown）。"""
        return self._get(f"/repos/{namespace}/docs/{slug}", raw=1)


def export_from_api(
    namespace: str | None = None,
    out_dir: Path = RAW_DIR,
    sleep: float = 0.3,
) -> list[Path]:
    """通过 OpenAPI 拉取整个知识库到本地 .md。"""
    namespace = namespace or config.yuque_namespace
    if not namespace:
        raise ValueError("缺少 YUQUE_NAMESPACE，请在 .env 中配置或传入 namespace。")

    out_dir.mkdir(parents=True, exist_ok=True)
    client = YuqueClient()
    docs = client.list_docs(namespace)
    print(f"知识库 {namespace} 共 {len(docs)} 篇文档，开始导出 -> {out_dir}")

    written: list[Path] = []
    for doc in tqdm(docs, desc="导出文档"):
        slug = doc.get("slug")
        title = doc.get("title", slug)
        try:
            detail = client.get_doc(namespace, slug)
        except requests.HTTPError as e:
            print(f"  [跳过] {title} ({slug}): {e}")
            continue
        body = detail.get("body") or ""
        fpath = out_dir / _safe_filename(title, slug)
        header = f"# {title}\n\n<!-- source: yuque://{namespace}/{slug} -->\n\n"
        fpath.write_text(header + body, encoding="utf-8")
        written.append(fpath)
        time.sleep(sleep)

    print(f"导出完成：{len(written)} 篇 .md")
    return written


def import_local_package(src_dir: str | Path, out_dir: Path = RAW_DIR) -> list[Path]:
    """归整本地语雀 Markdown 导出包（递归收集 .md）。"""
    src = Path(src_dir)
    if not src.exists():
        raise FileNotFoundError(f"目录不存在：{src}")
    out_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for md in src.rglob("*.md"):
        dst = out_dir / md.name
        shutil.copy2(md, dst)
        written.append(dst)
    print(f"已归整本地 Markdown：{len(written)} 篇 -> {out_dir}")
    return written


def iter_raw_docs(raw_dir: Path = RAW_DIR) -> Iterator[tuple[str, str]]:
    """遍历已导出的 .md，yield (来源标识, 正文)。"""
    for md in sorted(raw_dir.glob("*.md")):
        yield md.name, md.read_text(encoding="utf-8")
