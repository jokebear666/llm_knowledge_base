# 语雀知识库转结构化题库

将语雀知识库中的非结构化/半结构化文档，批量转换为标准化、可刷题的结构化题库，落地到 Supabase（PostgreSQL + pgvector）。

这是[方案文档](语雀知识库转结构化题库.md)的落地实现。

## 流水线

```
语雀导出 → 分块解析（规则 + LLM）→ 质检去重 → 人工标注 → 回灌 → 转选择题 → 入库 Supabase(pgvector) → 刷题
export      parse                  qc        (人工)     review   to-choice  load
```

| 阶段 | 命令 | 模块 | 说明 |
|---|---|---|---|
| ① 导出 | `export` | `exporter.py` | 语雀 OpenAPI 拉取（自动翻页），或归整本地 Markdown 包，统一为 `data/raw/*.md` |
| ② 解析 | `parse` | `chunker.py` + `parser.py` + `llm.py` | 长文按标题分块；规则解析显式问答、散文交给 LLM 抽取；硬规则一票否决 + LLM 反思过滤（7 维）；默认 4 并发、断点续跑 |
| ③ 质检 | `qc` | `qc.py` | 精确去重 + embedding 语义去重；导出人工抽检 TSV |
| ④ 标注 | （人工） | — | 在 TSV 的 `reviewed_OK` 列填 1/0，可直接修改答案 |
| ⑤ 回灌 | `review` | `qc.py` | 读回标注 TSV，丢弃标 0 的题、采纳人工修改，产出最终入库源 |
| ⑥ 转选择题 | `to-choice` | `choice.py` + `llm.py` | 每道问答题调一次 LLM，判定单选/多选并生成选项（正确项 + 似是而非干扰项）；默认 4 并发、断点续跑 |
| ⑦ 入库 | `load` | `loader.py` | 题目 + 选择题选项 + 题干 embedding upsert 到 Supabase |

## 安装

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # 填入语雀 Token、LLM Key、Supabase 连接串
```

## 统一题目结构

| 字段 | 说明 |
|---|---|
| `id` | 题干指纹（自动生成） |
| `type` | 八股 / 面经 / 算法 |
| `question` / `answer` | 题干 / 参考答案 |
| `category` / `tags` / `difficulty` | 分类 / 标签 / 难度（为薄弱点推荐打基础） |
| `question_kind` | 提问角度类型：区别对比类 / 原理机制类 / 作用目的类 / 动机原因类 / 场景适用类 / 方法实践类 / 定义概念类 / 优缺点取舍类 / 分类构成类 / 步骤流程类 / 其他（按题干句式自动判定） |
| `interview_fit` | 面试适合度：高频 / 中频 / 低频 / 无效（由 `question_kind` 推导） |
| `source_doc` | 来源文档（便于溯源回查） |
| `choice_kind` | 选择题类型：单选 / 多选（由 `to-choice` 生成；未转换时为空，仍可作开放问答） |
| `options` | 选择题选项（已打乱顺序），每项 ≤100 字 |
| `correct_index` | 正确选项下标（单选长度 1，多选 ≥2）；`answer` 字段保留完整原文作答案解析 |

## 使用

```bash
# 0. 初始化 Supabase 表（含 pgvector），首次执行；或直接在 SQL Editor 跑 sql/schema.sql
python -m quiz_pipeline.cli init-db

# 1. 导出：从语雀 OpenAPI（读 .env 的 namespace）
python -m quiz_pipeline.cli export --namespace user/repo
#    或归整本地语雀 Markdown 导出包
python -m quiz_pipeline.cli export --local ./yuque_export_dir

# 2. 解析（默认 4 并发调用 LLM，支持断点续跑；--no-llm 可仅用规则）
python -m quiz_pipeline.cli parse                 # 默认并发 4
python -m quiz_pipeline.cli parse --concurrency 8 # 提高并发（注意网关限流）
# 中途失败/中断后重跑同一命令即可，已完成的块会自动跳过（断点续跑）

# 3. 质检去重，产出 data/qc/review_sheet.tsv 供人工核对
python -m quiz_pipeline.cli qc

# 4. 人工打开 review_sheet.tsv 标注：reviewed_OK 列填 1(保留)/0(淘汰)，可直接修改答案

# 5. 回灌人工标注，产出最终入库源（丢弃标0的题、采纳人工修改）
python -m quiz_pipeline.cli review

# 6. 转选择题：每道题判定单选/多选并生成选项，产出 data/qc/choice_questions.json
python -m quiz_pipeline.cli to-choice                 # 默认并发 4、断点续跑
python -m quiz_pipeline.cli to-choice --no-resume     # 改了 prompt 后全量重生成

# 7. 入库（用带选择题字段的最终源）
python -m quiz_pipeline.cli load -i data/qc/choice_questions.json
```

一键串联导出→解析→质检（入库前留人工质检环节）：

```bash
python -m quiz_pipeline.cli run --namespace user/repo
```

## 操作流程详解（每步输入 / 输出）

| 步骤 | 命令 | 输入 | 输出 |
|---|---|---|---|
| 0. 建表（首次） | `init-db` | `.env`、`sql/schema.sql` | Supabase `questions` 表（含 pgvector、索引、`match_questions` 函数） |
| 1. 导出 | `export` | 语雀知识库（Token+namespace）或本地 md 目录 | `data/raw/*.md` |
| 2. 解析 | `parse` | `data/raw/*.md` | `data/parsed/questions.json`、`data/parsed/.llm_cache.json`（续跑缓存） |
| 3. 质检 | `qc` | `data/parsed/questions.json` | `data/qc/review_sheet.tsv`（人工标注用）、`deduped_questions.json`、`embeddings.json`、`dedup_report.json`、`review_questions.json` |
| 4. 标注 | （人工） | `data/qc/review_sheet.tsv` | 同文件（`reviewed_OK` 列填 1/0，可改答案） |
| 5. 回灌 | `review` | `data/qc/review_sheet.tsv`（已标注） | `data/qc/reviewed_questions_final.json` |
| 6. 转选择题 | `to-choice` | `reviewed_questions_final.json` | `data/qc/choice_questions.json`、`.choice_cache.json`（续跑缓存） |
| 7. 入库 | `load` | `choice_questions.json`（缺失时自动补 embedding） | Supabase `questions` 表记录（`reviewed=true`，含选择题字段） |

各步要点：

- **解析（parse）**：分块 → 规则解析(命中 `Q:/答:`) + LLM 抽取(散文) → 硬规则一票否决（背景/时间线/谁提出/指代外部语境等命中即删）→ LLM 反思过滤（技术相关性/收敛性/客观性/面试真实性/自包含性/答案质量/细节粒度 7 维）。改了 prompt 后需 `--no-resume` 才会重抽。
- **标注（人工）**：`reviewed_OK(1/0)` 列填 `1` 保留 / `0` 淘汰，留空默认保留；可直接修改 `question`/`answer`/`difficulty`/`category`/`tags`。
- **回灌（review）**：丢弃标 0 的题、采纳人工修改（改题干会重算 `id`）。题目数变化后与旧 `embeddings.json` 不再对齐，`load` 会自动重算 embedding，不会错位。
- **转选择题（to-choice）**：LLM 按答案内容自动判定单选/多选——结论唯一的做单选（1 正确项 + 3 干扰项），“有哪些/区别/优缺点/组成”等天然多要点的做多选（正确项数量按实际，不设上限）。正确项与干扰项均压缩到 100 字以内，干扰项要求“似是而非”以防一眼看穿；选项顺序按题目 `id` 稳定打乱。原始完整答案保留在 `answer` 字段作答案解析。改了 prompt 后需 `--no-resume` 才会用新 prompt 重生成。

常用开关：

- `parse --concurrency N` 调并发；`--no-llm` 仅规则；`--no-resume` 忽略缓存重跑；`--no-reflect` 关闭反思过滤
- `qc --no-semantic` 跳过语义去重；`--threshold 0.9` 调相似度阈值
- `to-choice --concurrency N` 调并发；`--no-resume` 忽略缓存全量重生成；`-i/-o` 自定义输入输出
- `load --unreviewed` 标记为未质检入库（默认按已质检 `reviewed=true`）

## 小批量验证（无需任何 Key）

仓库内置示例文档，可用纯规则路径跑通解析与质检：

```bash
python -m quiz_pipeline.cli export --local examples
python -m quiz_pipeline.cli parse --no-llm
python -m quiz_pipeline.cli qc --no-semantic
```

## 薄弱点 → 题目推荐

入库后，`sql/schema.sql` 提供 `match_questions(query_embedding, match_count, filter_category, filter_interview_fit)` 函数，
对题干 embedding 做余弦近邻检索，支撑「薄弱点 → 相似题目推荐」。可按 `category`、`interview_fit`（如只推「高频」题）过滤。

```sql
-- 只刷高频面试题
select * from questions where interview_fit = '高频' and reviewed = true;
-- 按提问类型出卷
select * from questions where question_kind = '区别对比类' and reviewed = true;
```

## 注意

- 质检是关键风险点：八股答案准确性影响口碑，AI 抽取/生成的题目**务必经人工抽检后再入库**，宁可少而精。
- embedding 用开源本地模型（`sentence-transformers`，默认 `BAAI/bge-small-zh-v1.5`，首次运行自动下载），无需调用付费 API。
- 建表 SQL 中 `vector(512)` 维度需与 `.env` 的 `EMBEDDING_DIM` 及所选模型一致；换模型记得同步改 SQL。
