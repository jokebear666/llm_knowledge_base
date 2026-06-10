"""LLM 与 embedding 调用封装。

大模型调用参考项目内 `llm_client.py` 的 AzureGPTClient 实现：
- 通过 langchain_openai.AzureChatOpenAI + responses API 调用；
- 懒加载模型，避免 import 即要求 langchain/网络/密钥；
- API key 优先取环境变量 GPT_AK / OPENAI_API_KEY；
- 输出用 json_repair 稳健解析 JSON。
"""
from __future__ import annotations

import json
import os
import re
from typing import Any, Optional

from .config import config

try:
    import json_repair  # type: ignore
except Exception:  # pragma: no cover
    json_repair = None  # type: ignore

EXTRACT_SYSTEM_PROMPT = """你是资深面试出题专家。你的任务是从给定的知识内容中，提炼/生成高质量面试题。

要求：
1. 只依据给定内容，不要编造内容中没有的事实；八股答案务必准确，宁缺毋滥。
2. 若内容本身已是问答结构，则抽取已有题目；若是散文/笔记，则反向生成考点题目。
3. 每道题包含字段：question(题干)、answer(标准答案/参考解析)、category(分类)、tags(标签数组)、difficulty(易/中/难)、type(八股/面经/算法)。
4. answer 要完整、可直接作为参考答案，必要时分点说明。
5. 严格以 JSON 输出，格式为 {"questions": [ {...}, ... ]}，不要输出任何额外文字。
6. 内容质量不足以出题时，返回 {"questions": []}。"""

EXTRACT_USER_TEMPLATE = """分类提示（来自文档标题路径，可参考）：{heading}
来源文档：{source_doc}

知识内容如下：
---
{content}
---

请仅输出 JSON，格式 {{"questions": [...]}}。"""


def _extract_json(text: str) -> dict[str, Any]:
    """从模型输出里稳健解析 JSON 对象（优先 json_repair）。"""
    if json_repair is not None:
        try:
            obj = json_repair.loads(text)
            if isinstance(obj, dict):
                return obj
            if isinstance(obj, list):
                return {"questions": obj}
        except Exception:
            pass
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    return {}


class AzureGPTClient:
    """参考 llm_client.py 的 Azure GPT client。

    懒加载 AzureChatOpenAI；满足 infer(prompt) -> str（返回含 JSON 的文本）。
    """

    _DEFAULT_KEY = "RLJ8QGWCL9ELlc8rc38o4hrvvqADk8EL_GPT_AK"

    def __init__(
        self,
        azure_endpoint: str = "https://gpt-i18n.byteintl.net/gpt/openapi/online/responses",
        api_version: str = "2024-03-01-preview",
        deployment_name: str | None = None,
        timeout: int = 120,
        max_tokens: int = 16384,
    ) -> None:
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", azure_endpoint)
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", api_version)
        self.deployment_name = deployment_name or config.llm_model
        self.timeout = timeout
        self.max_tokens = max_tokens
        self._model = None  # 懒加载

    def _api_key(self) -> str:
        return os.getenv("GPT_AK") or os.getenv("OPENAI_API_KEY") or self._DEFAULT_KEY

    def _ensure_model(self):
        if self._model is None:
            from langchain_openai import AzureChatOpenAI  # 懒导入

            self._model = AzureChatOpenAI(
                azure_endpoint=self.azure_endpoint,
                openai_api_version=self.api_version,
                deployment_name=self.deployment_name,
                openai_api_key=self._api_key(),
                openai_api_type="azure",
                use_responses_api=True,
                temperature=0,
                timeout=self.timeout,
                max_tokens=self.max_tokens,
            )
        return self._model

    def infer(self, prompt: str, system: Optional[str] = None) -> str:
        from langchain_core.messages import AIMessage, HumanMessage, SystemMessage  # 懒导入

        messages: list[Any] = []
        if system:
            messages.append(SystemMessage(content=system))
        messages.append(HumanMessage(content=[{"type": "text", "text": prompt}]))

        response = self._ensure_model().invoke(messages)
        content = response.content if isinstance(response, AIMessage) else str(response)
        if isinstance(content, list):  # responses API 可能返回分段内容
            parts: list[str] = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    parts.append(part["text"])
                elif isinstance(part, str):
                    parts.append(part)
            content = " ".join(parts)
        return content


class LocalEmbedder:
    """开源本地 embedding（sentence-transformers）。

    默认 BAAI/bge-small-zh-v1.5（中文友好、512 维、体积小，CPU 可跑）。
    懒加载模型，归一化输出便于直接做余弦相似度与 pgvector cosine 检索。
    """

    def __init__(self, model_name: str | None = None) -> None:
        self.model_name = model_name or config.embedding_model
        self._model = None  # 懒加载

    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer  # 懒导入

            self._model = SentenceTransformer(self.model_name)
        return self._model

    @property
    def dim(self) -> int:
        return self._ensure_model().get_sentence_embedding_dimension()

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vecs = self._ensure_model().encode(
            texts,
            normalize_embeddings=True,  # 归一化，余弦相似度即点积
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return vecs.tolist()


class LLMClient:
    """对外统一接口：抽取题目 + 生成 embedding。

    - 抽取走 AzureGPTClient（参考 llm_client.py）。
    - embedding 走开源本地模型 LocalEmbedder（sentence-transformers）。
    """

    def __init__(self) -> None:
        self.chat = AzureGPTClient()
        self.embedding_model = config.embedding_model
        self.embedder = LocalEmbedder(self.embedding_model)

    def extract_questions(self, content: str, heading: str, source_doc: str) -> list[dict[str, Any]]:
        """从一个内容块抽取/生成题目，稳健解析 JSON。"""
        user = EXTRACT_USER_TEMPLATE.format(heading=heading, source_doc=source_doc, content=content)
        raw = self.chat.infer(user, system=EXTRACT_SYSTEM_PROMPT)
        data = _extract_json(raw)
        items = data.get("questions", data if isinstance(data, list) else [])
        return items if isinstance(items, list) else []

    def embed(self, texts: list[str]) -> list[list[float]]:
        """批量生成 embedding（开源本地模型）。"""
        return self.embedder.embed(texts)

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]
