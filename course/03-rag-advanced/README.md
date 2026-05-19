# Module 03 — Advanced RAG

**Goal:** take the naive RAG from module 02 and make it actually good. Hybrid search, reranking, query rewriting, and a real eval framework (RAGAS).

---

## What you'll ship

- `pipeline.py` — a configurable RAG pipeline where each stage (retrieve, rerank, generate) can be swapped.
- Hybrid retrieval: dense (embeddings) + sparse (BM25) with score fusion (RRF — Reciprocal Rank Fusion).
- A reranker pass using either Cohere Rerank API or a local cross-encoder (`BAAI/bge-reranker-base`).
- Query rewriting: an LLM step that turns "what about cooling?" into a better retrieval query, or splits a multi-hop question.
- RAGAS evaluation: faithfulness, answer relevance, context recall, context precision.

---

## Key concepts

- **Dense vs sparse retrieval** — embeddings catch semantic matches; BM25 catches exact-term matches. Hybrid wins.
- **RRF** — combine ranked lists from N retrievers without needing comparable scores.
- **Cross-encoder reranking** — second-stage model that re-scores top-N candidates with much higher accuracy than dense alone. Slower → only on candidates, not the whole corpus.
- **Query transformations** — HyDE, multi-query, decomposition. Pick one and learn it well before sprinkling more.
- **RAGAS metrics** — automate what you were eyeballing in module 02.

---

## Reference links

- RAGAS: https://docs.ragas.io/
- BM25 in LangChain: https://python.langchain.com/docs/integrations/retrievers/bm25/
- Cohere Rerank: https://docs.cohere.com/docs/rerank-overview
- BGE Reranker: https://huggingface.co/BAAI/bge-reranker-base
- "Advanced RAG" (LlamaIndex blog series): https://www.llamaindex.ai/blog
- HyDE paper: https://arxiv.org/abs/2212.10496

---

## Steps

1. Copy your `data/raw/` and the Chroma DB from module 02 (or re-ingest).
2. Add BM25 retriever over the same chunks; combine with dense via RRF.
3. Add a reranker stage: take top-30 from hybrid → rerank → take top-5.
4. Write a query-rewriting prompt (LLM step) and toggle it on/off via config.
5. Build a clean RAGAS eval set (~25 Q/A with reference contexts).
6. Run RAGAS on four configs: naive (from M02), +hybrid, +hybrid+rerank, +hybrid+rerank+rewrite. Table the results.
7. Pick the config that wins on faithfulness + context recall together (not just one metric).

---

## What "done" looks like

- A single config flip (e.g. `--rerank=bge`) switches the pipeline stages.
- RAGAS table shows monotonic improvement from naive → final.
- You can articulate when the reranker isn't worth its latency cost.

---

## Stretch

- Add semantic chunking using embeddings to find natural breakpoints (LangChain `SemanticChunker`).
- Try a self-querying retriever that filters by metadata it infers from the question.
- Replace Chroma with pgvector + Postgres; benchmark on a 100k-chunk corpus.

---

## Production angle

This is what most "RAG in production" teams actually run: hybrid retrieval + reranker + judged evals on every change. You're not learning a toy version anymore.
