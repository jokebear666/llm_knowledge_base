"""PromptNode 使用的多模态 LLM 封装。

职责：
1. 多模态格式化：把文本 prompt 与图像/视频引用组装成模型请求。
2. 推理：低 temperature + 多次采样（对抗随机性）。
3. JSON 抽取：从模型输出里稳健地解析 JSON（优先 json_repair）。

默认使用 MockLLM，便于在无真实模型 API 的环境下跑通全流程。接入真实模型时，
实现一个满足 `infer(prompt, images, model, temperature) -> str` 的 client，
通过 `set_llm_client` 注入即可。
"""

from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any, Dict, List, Optional, Protocol

try:
    import json_repair  # type: ignore
except Exception:  # pragma: no cover
    json_repair = None  # type: ignore


class LLMClient(Protocol):
    def infer(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        model: str = "ValleyPro",
        temperature: float = 0.01,
    ) -> str:
        ...


# 信号关键字触发表：key -> 命中即判 True 的内容子串（小写匹配）。
# 仅用于离线 demo 的确定性复现；真实环境请注入实际多模态模型 client。
KEY_TRIGGERS: Dict[str, List[str]] = {
    # —— 虚假价格（保留向后兼容）——
    "has_strikethrough": ['"was"', "现价", "now "],
    "has_absolute_claim": ["全网最低", "史上最低", "最低价", "lowest"],
    "was_verified": ['"was_verified": true', "已核实"],
    "official_promo": ['"official_promo": true', "官方大促"],
    # —— Gambling 豁免/出界 ——
    "genv_out_of_scope": ["financial investment", "stocks", "crypto", "casino themed party", "casino-themed party"],
    "genv_sports_gambling": ["horse race", "sports gambling", "sports betting"],
    "genv_media_context": ["news", "movie", "tv show", "music video", "documentary", "educational", "awareness", "humour", "humor", "skit", "meme", "highlight"],
    "genv_merchandise_only": ["merchandise", "accessories"],
    "genv_no_monetary_recreational": ["recreational", "without bet", "no bet", "at home", "magic trick", "non gambling environment", "non-gambling"],
    # —— Gambling 违规要素 ——
    "gambling_elements_present": ["casino", "poker", "roulette", "slot machine", "betting", "chips", "mahjong", "pachinko", "lottery", "toto", "4d", "gambling", "wager", "odds", "blackjack", "dice"],
    # —— Gamification 领域/类型 ——
    "is_gamification": ["spin wheel", "lucky spin", "golden egg", "surprise egg", "lucky egg", "lucky pull", "giveaway", "claw machine", "crane game", "arcade", "puzzle", "trivia", "quiz", "mystery box", "lucky scoop", "blind box", "gachapon", "advent calendar", "lucky draw", "balloon game", "racing game", "gamification", "scoop", "collectible", "card"],
    "game_skill_based": ["arcade", "claw machine", "crane", "puzzle", "memory game", "trivia", "quiz", "skill"],
    "game_chance_based": ["spin", "lucky egg", "golden egg", "surprise egg", "lucky pull", "mystery box", "lucky scoop", "lucky draw", "balloon", "racing game", "chance", "random"],
    # —— Gamification 违规 ——
    "prize_is_cash_or_luxury": ["cash prize", "money prize", "smartphone", "iphone", "tablet", "gaming console", "designer", "luxury", "branded watch", "jewelry"],
    "paid_to_participate": ["pay to play", "payment to join", "paid entry", "pay to try", "direct payment", "pay to participate", "payment required"],
    "prize_value_unknown": ["mystery box", "lucky scoop", "variable prize", "unknown prize", "randomized prize"],
    "commercialized_collectibles": ["contact number to buy", "commercialise", "commercialize", "for resale", "resale", "where to buy"],
    "commercial_profit_driven": ["profit-driven", "commercial game", "money scooping", "monetiz"],
    # —— Gamification 豁免 ——
    "linked_to_purchase_or_free_join": ["with purchase", "comment to win", "no payment", "buy a product gives", "linked to purchase"],
    "prize_value_known": ["advent calendar", "blind box", "gachapon", "sure win", "known prize"],
    "personal_use_collectibles": ["personal collection", "pokemon", "pokémon", "personal hobby", "personal use"],
    "non_commercial_game": ["among friends", "casual game", "non commercialise", "non-commercial"],
    "incidental": ["background", "incidental", "not the highlight"],
}


class MockLLM:
    """Schema 驱动的确定性 mock。

    1) 从 prompt 的"输出JSON:"片段解析被请求的字段及其声明类型；
    2) bool 字段按 KEY_TRIGGERS 在"内容部分"(输出JSON 之前) 做关键字命中；
    3) 数值字段：confidence 固定 0.9，prize_value_usd 等从内容里解析金额。

    仅用于离线跑通与单测；真实环境请注入实际模型 client。
    """

    def infer(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        model: str = "ValleyPro",
        temperature: float = 0.01,
    ) -> str:
        marker = "输出JSON" if "输出JSON" in prompt else "Output JSON"
        content = prompt.split(marker)[0]
        lc = content.lower()

        requested = re.findall(r'"(\w+)"\s*:\s*(bool|float|int|number|str)', prompt)
        result: Dict[str, Any] = {}
        for key, typ in requested:
            if typ == "bool":
                triggers = KEY_TRIGGERS.get(key, [])
                result[key] = any(t in lc for t in triggers)
            elif typ in ("float", "int", "number"):
                if key == "confidence":
                    result[key] = 0.9
                else:
                    result[key] = _extract_number(content, key)
            else:  # str
                result[key] = ""
        if "confidence" not in result:
            result["confidence"] = 0.9
        return json.dumps(result, ensure_ascii=False)


def _extract_number(content: str, key: str) -> float:
    m = re.search(r'"%s"\s*:\s*([0-9.]+)' % re.escape(key), content)
    if m:
        return float(m.group(1))
    m = re.search(r"\$\s*([0-9.]+)", content)
    if m:
        return float(m.group(1))
    m = re.search(r"([0-9.]+)\s*usd", content, re.I)
    if m:
        return float(m.group(1))
    return 0.0


class AzureGPTClient:
    """真实多模态模型 client：复用 graph.py 中的 Azure GPT-5.4 配置。

    - 满足 LLMClient 协议：infer(prompt, images, model, temperature) -> str（返回含 JSON 的文本，
      由上层 extract_json + majority_vote 解析）。
    - 懒加载：首次 infer 时才构造 AzureChatOpenAI，避免 import core 即要求 langchain/网络/密钥
      （check_workflow 等离线工具仅 import 不调用，不受影响）。
    - API key 优先取环境变量 GPT_AK / OPENAI_API_KEY，缺省回落到 graph.py 内置值（建议用 env 覆盖）。
    """

    _DEFAULT_KEY = "RLJ8QGWCL9ELlc8rc38o4hrvvqADk8EL_GPT_AK"

    def __init__(
        self,
        azure_endpoint: str = "https://gpt-i18n.byteintl.net/gpt/openapi/online/responses",
        api_version: str = "2024-03-01-preview",
        deployment_name: str = "gpt-5.4-2026-03-05",
        timeout: int = 120,
        max_tokens: int = 16384,
    ) -> None:
        self.azure_endpoint = azure_endpoint
        self.api_version = api_version
        self.deployment_name = deployment_name
        self.timeout = timeout
        self.max_tokens = max_tokens
        self._model = None  # 懒加载

    def _ensure_model(self):
        if self._model is None:
            import os

            from langchain_openai import AzureChatOpenAI  # 懒导入

            api_key = (
                os.getenv("GPT_AK")
                or os.getenv("OPENAI_API_KEY")
                or self._DEFAULT_KEY
            )
            self._model = AzureChatOpenAI(
                azure_endpoint=self.azure_endpoint,
                openai_api_version=self.api_version,
                deployment_name=self.deployment_name,
                openai_api_key=api_key,
                openai_api_type="azure",
                use_responses_api=True,
                temperature=0,
                timeout=self.timeout,
                max_tokens=self.max_tokens,
            )
        return self._model

    def infer(
        self,
        prompt: str,
        images: Optional[List[str]] = None,
        model: str = "ValleyPro",
        temperature: float = 0.01,
    ) -> str:
        from langchain_core.messages import AIMessage, HumanMessage  # 懒导入

        message_content: List[Dict[str, Any]] = []
        for img_url in images or []:
            message_content.append({"type": "image_url", "image_url": {"url": img_url}})
        message_content.append({"type": "text", "text": prompt})

        response = self._ensure_model().invoke([HumanMessage(content=message_content)])
        content = response.content if isinstance(response, AIMessage) else str(response)
        if isinstance(content, list):  # responses API 可能返回分段内容
            parts: List[str] = []
            for part in content:
                if isinstance(part, dict) and "text" in part:
                    parts.append(part["text"])
                elif isinstance(part, str):
                    parts.append(part)
            content = " ".join(parts)
        return content


def _default_client() -> LLMClient:
    """默认 client：除非显式设 AUTOWORKFLOW_LLM=mock，否则使用真实 GPT-5.4。"""
    import os

    if os.getenv("AUTOWORKFLOW_LLM", "").strip().lower() == "mock":
        return MockLLM()
    return AzureGPTClient()


_CLIENT: LLMClient = _default_client()


def set_llm_client(client: LLMClient) -> None:
    global _CLIENT
    _CLIENT = client


def render(template: str, variables: Dict[str, Any]) -> str:
    """极简模板渲染：把 {key} 替换为对应特征值的字符串形式。"""
    out = template
    for key, value in variables.items():
        out = out.replace("{" + key + "}", _stringify(value))
    return out


def _stringify(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def extract_json(text: str) -> Dict[str, Any]:
    """从模型输出里稳健解析 JSON 对象。"""
    if json_repair is not None:
        try:
            obj = json_repair.loads(text)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
    # 退化路径：抓取第一个 {...} 片段
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            pass
    raise ValueError(f"cannot extract JSON from LLM output: {text[:200]}")


def majority_vote(samples: List[Dict[str, Any]]) -> Dict[str, Any]:
    """对多次采样的结构化输出做字段级多数投票，降低单次扰动。"""
    if not samples:
        return {}
    if len(samples) == 1:
        return samples[0]
    keys = set().union(*[s.keys() for s in samples])
    voted: Dict[str, Any] = {}
    for key in keys:
        values = [_hashable(s.get(key)) for s in samples if key in s]
        most_common, _ = Counter(values).most_common(1)[0]
        voted[key] = _unhashable(most_common)
    return voted


def _hashable(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, ensure_ascii=False)
    return value


def _unhashable(value: Any) -> Any:
    if isinstance(value, str) and value and value[0] in "[{":
        try:
            return json.loads(value)
        except Exception:
            return value
    return value


def infer_structured(
    prompt: str,
    images: Optional[List[str]],
    model: str,
    temperature: float,
    n_sample: int = 1,
) -> Dict[str, Any]:
    """低温 + 多采样 + JSON 抽取 + 多数投票，返回单个结构化结果。"""
    samples: List[Dict[str, Any]] = []
    for _ in range(max(1, n_sample)):
        raw = _CLIENT.infer(prompt, images=images, model=model, temperature=temperature)
        samples.append(extract_json(raw))
    return majority_vote(samples)
