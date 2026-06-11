-- 语雀知识库转结构化题库 · Supabase 建表（含 pgvector）
-- 在 Supabase SQL Editor 中执行。
-- 注意：vector(512) 维度需与 .env 的 EMBEDDING_DIM / 所选开源 embedding 模型一致。
-- 默认 BAAI/bge-small-zh-v1.5 = 512 维；换模型时同步修改下方 vector(N) 与 match_questions 参数。

create extension if not exists vector;

create table if not exists questions (
    id          text primary key,                 -- 题干指纹（见 models.Question.fingerprint）
    type        text not null default '八股',      -- 八股 / 面经 / 算法
    question    text not null,
    answer      text not null,
    category    text not null default '未分类',
    tags        text[] not null default '{}',
    difficulty  text not null default '中',        -- 易 / 中 / 难
    question_kind text not null default '其他',      -- 提问角度类型（区别对比类/原理机制类/...）
    interview_fit text not null default '无效',      -- 面试适合度：高频 / 中频 / 低频 / 无效
    source_doc  text not null default '',
    choice_kind   text,                            -- 选择题类型：单选 / 多选（NULL=未转选择题）
    options       text[] not null default '{}',    -- 选择题选项（已打乱顺序）
    correct_index int[]  not null default '{}',    -- 正确选项下标（单选长度1，多选>=2）
    embedding   vector(512),                       -- 题干 embedding，用于语义推荐/去重
    reviewed    boolean not null default false,    -- 人工质检是否通过
    created_at  timestamptz not null default now(),
    updated_at  timestamptz not null default now()
);

-- 兼容已建表：补齐选择题相关列（首次建表时这些列已存在，alter 为幂等）
alter table questions add column if not exists choice_kind   text;
alter table questions add column if not exists options       text[] not null default '{}';
alter table questions add column if not exists correct_index int[]  not null default '{}';

create index if not exists idx_questions_category on questions (category);
create index if not exists idx_questions_type     on questions (type);
create index if not exists idx_questions_tags      on questions using gin (tags);
create index if not exists idx_questions_kind      on questions (question_kind);
create index if not exists idx_questions_fit       on questions (interview_fit);

-- 语义检索向量索引（题量大时建议 ivfflat / hnsw）
create index if not exists idx_questions_embedding
    on questions using ivfflat (embedding vector_cosine_ops) with (lists = 100);

-- 「薄弱点 -> 题目推荐」语义检索函数：按题干向量找最相似的题目。
create or replace function match_questions(
    query_embedding vector(512),
    match_count int default 10,
    filter_category text default null,
    filter_interview_fit text default null
)
returns table (
    id text,
    question text,
    answer text,
    category text,
    tags text[],
    difficulty text,
    question_kind text,
    interview_fit text,
    similarity float
)
language sql stable
as $$
    select q.id, q.question, q.answer, q.category, q.tags, q.difficulty,
           q.question_kind, q.interview_fit,
           1 - (q.embedding <=> query_embedding) as similarity
    from questions q
    where q.embedding is not null
      and q.reviewed = true
      and (filter_category is null or q.category = filter_category)
      and (filter_interview_fit is null or q.interview_fit = filter_interview_fit)
    order by q.embedding <=> query_embedding
    limit match_count;
$$;
