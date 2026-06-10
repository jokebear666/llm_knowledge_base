# 语雀知识库转结构化题库

将语雀知识库中的非结构化/半结构化文档，批量转换为标准化、可刷题的结构化题库，落地到 Supabase（PostgreSQL + pgvector）。

这是[方案文档](语雀知识库转结构化题库.md)的落地实现。

## 流水线

```
语雀导出 → 分块解析（规则 + LLM）→ 人工质检去重 → 入库 Supabase(pgvector) → 刷题
```

| 阶段 | 模块 | 说明 |
|---|---|---|
| ① 导出 | `exporter.py` | 语雀 OpenAPI 拉取，或归整本地 Markdown 包，统一为 `data/raw/*.md` |
| ② 解析 | `chunker.py` + `parser.py` + `llm.py` | 长文按标题分块；规则解析显式问答，散文交给 LLM 强制 JSON 抽取 |
| ③ 质检 | `qc.py` | 精确去重 + embedding 语义去重；导出人工抽检 CSV |
| ④ 入库 | `loader.py` | 题目 + 题干 embedding upsert 到 Supabase |

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
| `source_doc` | 来源文档（便于溯源回查） |

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

# 3. 质检去重，产出 data/qc/review_sheet.csv 供人工核对
python -m quiz_pipeline.cli qc

# 4. 人工核对无误后入库
python -m quiz_pipeline.cli load -i data/qc/deduped_questions.json
```

一键串联导出→解析→质检（入库前留人工质检环节）：

```bash
python -m quiz_pipeline.cli run --namespace user/repo
```

## 小批量验证（无需任何 Key）

仓库内置示例文档，可用纯规则路径跑通解析与质检：

```bash
python -m quiz_pipeline.cli export --local examples
python -m quiz_pipeline.cli parse --no-llm
python -m quiz_pipeline.cli qc --no-semantic
```

## 薄弱点 → 题目推荐

入库后，`sql/schema.sql` 提供 `match_questions(query_embedding, match_count, filter_category)` 函数，
对题干 embedding 做余弦近邻检索，支撑「薄弱点 → 相似题目推荐」。

## 注意

- 质检是关键风险点：八股答案准确性影响口碑，AI 抽取/生成的题目**务必经人工抽检后再入库**，宁可少而精。
- embedding 用开源本地模型（`sentence-transformers`，默认 `BAAI/bge-small-zh-v1.5`，首次运行自动下载），无需调用付费 API。
- 建表 SQL 中 `vector(512)` 维度需与 `.env` 的 `EMBEDDING_DIM` 及所选模型一致；换模型记得同步改 SQL。
