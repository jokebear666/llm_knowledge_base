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
import time
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
3. 每道题包含字段：question(题干)、answer(标准答案/参考解析)、tags(标签数组)、difficulty(易/中/难)、type(八股/面经/算法)。不要输出 category 字段（分类由系统按文档归属自动填充）。
4. answer 要完整、可直接作为参考答案，必要时分点说明。
5. 严格以 JSON 输出，格式为 {"questions": [ {...}, ... ]}，不要输出任何额外文字。
6. 内容质量不足以出题时，返回 {"questions": []}。

【出题方向（重要）】
1. 只从算法原理、算法技术、工程实现、机制细节等专业硬核角度提问。例如：原理是什么、如何实现、为什么这样设计、计算过程、复杂度、参数作用、组件职责、技术取舍等。
2. 严禁出发散式/开放式问题：不要问背景、发展历史、时间线、提出动机、设计理念、目标意义、价值影响、前景展望、"为什么重要"这类没有唯一答案的题。
3. 每道题必须有明确、确定、可对照的答案。无法从内容中得到确定答案的，不要出题。如果某段内容只讲背景/理念/价值而没有可考的技术点，就跳过它（返回更少的题甚至空数组），不要硬凑。

【题库自洽性 / 自包含性】题目和答案必须是脱离原文档也成立的通用知识——换一个来源也对。禁止出现"文中/根据材料/该报告/本文/如上图/上文/本节"等指代原文出处的表述，禁止只在某篇文档语境下才成立的题。把"文中指出"改成直接陈述结论。读者看不到原文，只看到题目本身。

【避免重复】同一个知识点只出一道最有代表性的题，不要换个问法重复考查同一内容；优先覆盖不同考点而非堆叠数量。

【避免过细（重要）】只考面试常考的核心思想、原理、设计动机与取舍，不要钻进代码/公式的实现级细节。以下这类“太细”的题严禁生成：
- 具体变量名/张量符号/下标区间的含义，例如“下标区间 2+k:T+1 表示什么”“h_i^k 对应哪个位置”。
- 某一行代码/某个具体写法为什么这么写，例如“为什么除以 completion_mask.sum()”。
- 某个量是如何一步步算出来的等纯推导/实现步骤细节。
判断标准：如果一道题脱离这篇文档的具体符号/代码就无法理解或没有意义，就是太细，不要出。应把它抽象成考“原理/动机/设计”的题（例如不问“为什么除以 completion_mask.sum()”，而问“计算 KL 和 clip ratio 时为什么要按有效 token 数做归一化”）。

【难度判定标准】严格按以下锚点标注 difficulty：
- 易：单一技术概念/定义/参数含义的准确复述。
- 中：多个技术要点的对比、分类，或具体实现步骤、计算/推导过程。
- 难：机制原理深层推导、设计权衡、复杂度分析、优缺点取舍。
偏向如实评估，不要把需要对比/推导的题判为"易"。"""

EXTRACT_USER_TEMPLATE = """分类提示（来自文档标题路径，可参考）：{heading}
来源文档：{source_doc}

知识内容如下：
---
{content}
---

请仅输出 JSON，格式 {{"questions": [...]}}。"""


# ===== 反思过滤：抽取后对每道题做合理性审查（LLM-as-judge）=====
REFLECT_SYSTEM_PROMPT = """你是严格的面试题质量审查官。你会收到若干道由 AI 抽取的面试题（含题干与答案），\
请逐题从以下 6 个维度判断它是否应当保留进题库。每个维度给出了【低分反例】与【高分特征】：

1. 技术相关性（考察是否考算法/技术知识本身）
   低分反例：考提出时间、谁提出、为什么火、行业动态。
   高分特征：考原理、机制、设计、权衡。
2. 收敛性（答案是否唯一/有限且确定）
   低分反例：“为什么会火”“有什么影响”等开放发散问题。
   高分特征：“X 和 Y 的区别”“为什么需要 X”这类有确定答案的问题。
3. 客观性（答案是否可判定对错）
   低分反例：含主观评价、趋势预测、立场判断。
   高分特征：有标准答案、事实/原理可验证。
4. 面试真实性（像不像真实面试会问的题）
   低分反例：考冷门时事、特定博客作者言论。
   高分特征：通用概念、可迁移的技术理解。
5. 自包含性（关键！脱离原文档能否成立）
   低分反例：依赖“本文”“该报告”等特定语境；答案只在某篇文档里成立。
   高分特征：题目+答案是通用知识，换一个来源也成立。
6. 答案质量（答案本身是否准确、完整、不啰嗦）
   低分反例：答非所问、信息缺失、纯罗列。
   高分特征：准确、结构清晰、有解释。
7. 细节粒度（是否考得太细，超出常规面试粒度）
   低分反例：问具体变量名/张量符号/下标区间含义（如“2+k:T+1 表示什么”“h_i^k 对应哪个位置”）；问某一行代码/某个写法为什么这么写（如“为什么除以 completion_mask.sum()”）；纯推导步骤、实现级细节；脱离这篇文档的具体符号/代码就无意义的题。
   高分特征：考核心思想、原理、设计动机与取舍，换个实现/框架依然成立。

判定标准：只有 7 个维度全部合格才保留（keep=true）；任一维度命中低分反例/明显不合格则过滤（keep=false）。从严把关，宁缺毋滥。

严格以 JSON 输出，格式：
{"results": [ {"index": 0, "keep": true, "reason": "简要理由(若过滤需指明命中哪个维度)"}, ... ]}
index 对应输入题目的序号（从 0 开始），results 必须覆盖每一道输入题。不要输出额外文字。"""

REFLECT_USER_TEMPLATE = """请审查以下 {n} 道题：

{questions_block}

请输出 JSON，格式 {{"results": [{{"index": 0, "keep": true/false, "reason": "..."}}, ...]}}。"""


# ===== 问答题 -> 单选题：基于题干与参考答案生成 1 正确 + 3 干扰 =====
TO_CHOICE_SYSTEM_PROMPT = """你是资深面试出题专家。你会收到一道问答题（题干 question + 参考答案 answer），\
请把它改造成一道**单选题**：恰好 1 个正确项 + 3 个干扰项，共 4 个选项。

【正确项要求】
- 只给 **1 个**正确项，它是参考答案中最核心的结论/定义/原理。
- 忠实于参考答案的含义，不改变事实，但**压缩到 100 字以内**：保留关键信息，去掉冗余修饰与举例，措辞尽量贴近原文。
- 若参考答案包含多个并列要点，则把它们**综合概括成一句**作为唯一正确项（不要拆成多条），其余细节由“答案解析”承载。

【干扰项要求（关键）】
- 恰好给 **3 个**干扰项。
- 似是而非：看起来合理、与题目同领域，但事实上是错误的（常见误解、易混淆概念、张冠李戴、以偏概全）。
- 不能与正确项语义重复，不能是“以上都对/都不对”。
- 长度、风格、详略与正确项接近（同样 ≤100 字），避免正确项明显更长/更完整而泄题。

注意：原始完整答案会另外保留作为“答案解析”，所以选项只需精炼到能判断对错即可，不必承载全部细节。

严格以 JSON 输出，不要任何额外文字：
{"choice_kind": "single", "correct": ["唯一正确项"], "distractors": ["干扰项1", "干扰项2", "干扰项3"]}
"""

TO_CHOICE_USER_TEMPLATE = """题干：{question}

参考答案：{answer}

请输出 JSON：{{"choice_kind": "single", "correct": ["唯一正确项"], "distractors": ["干扰1", "干扰2", "干扰3"]}}。"""


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

    def extract_questions(
        self,
        content: str,
        heading: str,
        source_doc: str,
        max_retries: int = 3,
    ) -> list[dict[str, Any]]:
        """从一个内容块抽取/生成题目，稳健解析 JSON。失败按指数退避重试。"""
        user = EXTRACT_USER_TEMPLATE.format(heading=heading, source_doc=source_doc, content=content)
        last_err: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
                raw = self.chat.infer(user, system=EXTRACT_SYSTEM_PROMPT)
                data = _extract_json(raw)
                items = data.get("questions", data if isinstance(data, list) else [])
                return items if isinstance(items, list) else []
            except Exception as e:  # 网络/限流/超时等
                last_err = e
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # 1s, 2s, 4s...
        raise RuntimeError(f"LLM 抽取失败（已重试 {max_retries} 次）：{last_err}")

    def reflect_filter(
        self,
        items: list[dict[str, Any]],
        max_retries: int = 2,
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
        """对一组抽取出的题目做反思审查，返回 (保留, 被过滤)。

        每个被过滤项附带 _drop_reason 便于人工回查。审查失败时保守保留全部，
        不因审查环节出错而误杀题目。
        """
        if not items:
            return [], []

        # 组装待审查文本（只给题干+答案，控制 token）
        lines = []
        for i, it in enumerate(items):
            q = (it.get("question") or "").strip()
            a = (it.get("answer") or "").strip()
            lines.append(f"[{i}] 题干：{q}\n    答案：{a}")
        user = REFLECT_USER_TEMPLATE.format(n=len(items), questions_block="\n\n".join(lines))

        results = None
        for attempt in range(max_retries):
            try:
                raw = self.chat.infer(user, system=REFLECT_SYSTEM_PROMPT)
                data = _extract_json(raw)
                results = data.get("results")
                if isinstance(results, list):
                    break
            except Exception:
                pass
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)

        if not isinstance(results, list):
            # 审查不可用时保守保留，避免误杀
            return items, []

        verdict: dict[int, dict] = {}
        for r in results:
            if isinstance(r, dict) and isinstance(r.get("index"), int):
                verdict[r["index"]] = r

        kept, dropped = [], []
        for i, it in enumerate(items):
            r = verdict.get(i)
            # 没有明确判 false 的默认保留（缺审查结果时从宽，避免误杀）
            if r is not None and r.get("keep") is False:
                it = dict(it)
                it["_drop_reason"] = r.get("reason", "")
                dropped.append(it)
            else:
                kept.append(it)
        return kept, dropped

    def to_choice(
        self,
        question: str,
        answer: str,
        max_retries: int = 3,
    ) -> Optional[dict[str, Any]]:
        """把一道问答题转成选择题。

        返回 {"choice_kind": "single"|"multiple", "correct": [...], "distractors": [...]}；
        解析失败/重试耗尽返回 None（调用方决定是否跳过）。
        """
        user = TO_CHOICE_USER_TEMPLATE.format(question=question, answer=answer)
        last_err: Optional[Exception] = None
        for attempt in range(max_retries):
            try:
                raw = self.chat.infer(user, system=TO_CHOICE_SYSTEM_PROMPT)
                data = _extract_json(raw)
                kind = str(data.get("choice_kind", "")).strip().lower()
                correct = data.get("correct") or []
                distractors = data.get("distractors") or []
                if kind in ("single", "multiple") and isinstance(correct, list) and isinstance(distractors, list):
                    correct = [str(c).strip() for c in correct if str(c).strip()]
                    distractors = [str(d).strip() for d in distractors if str(d).strip()]
                    if correct and distractors:
                        return {"choice_kind": kind, "correct": correct, "distractors": distractors}
            except Exception as e:
                last_err = e
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        if last_err is not None:
            raise RuntimeError(f"LLM 生成选择题失败（已重试 {max_retries} 次）：{last_err}")
        return None

    def embed(self, texts: list[str]) -> list[list[float]]:
        """批量生成 embedding（开源本地模型）。"""
        return self.embedder.embed(texts)

    def embed_one(self, text: str) -> list[float]:
        return self.embed([text])[0]
