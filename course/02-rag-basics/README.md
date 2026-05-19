# Module 02 — RAG over Your Docs

**Goal:** build a "chat with my PDFs" app end-to-end. Ingest → chunk → embed → store → retrieve → answer with citations.

This is the canonical Gen-AI app. Every Gen-AI engineer ships one. Yours will be honest about its limits — module 03 makes it actually good.

---

## What you'll ship

- `ingest.py` — point it at a folder of PDFs/MDs/TXTs → chunks → embeds → upserts into a vector DB.
- `ask.py` — CLI: ask a question → top-k retrieval → context + question to LLM → answer with `[source: file.pdf p.3]` citations.
- A small evaluation pass: do 10 hand-written Q&A pairs against your corpus; measure how often the citation is correct.

Use a **real corpus**: your own PDFs (papers, manuals, notes). Don't use a toy dataset — you have to feel the failures.

---

## Key concepts

- **Chunking** — sliding window vs recursive vs semantic. Size matters: too small loses context, too big dilutes retrieval.
- **Embeddings** — text → vector. We use OpenAI `text-embedding-3-small` (cheap, good) and Hugging Face `BAAI/bge-small-en-v1.5` (free, local).
- **Vector DB** — start with Chroma (zero-setup, in-process). Migrate to pgvector later when production calls.
- **Retrieval** — cosine similarity over the top-k chunks. Distance metric matters.
- **Grounding & citations** — the prompt must constrain the LLM to answer *only* from retrieved chunks, and to cite them.
- **RAG failure modes** — hallucination on missing info, wrong chunk retrieved, multi-hop questions failing. You'll meet all three.

---

## Reference links

- LangChain document loaders: https://python.langchain.com/docs/integrations/document_loaders/
- Chroma: https://docs.trychroma.com/
- pgvector: https://github.com/pgvector/pgvector
- OpenAI embeddings: https://platform.openai.com/docs/guides/embeddings
- Sentence Transformers (BGE etc.): https://huggingface.co/BAAI/bge-small-en-v1.5
- "Building RAG-based LLM Applications for Production" — Anyscale blog series.

---

## Steps

1. Set up project venv. `pip install` `langchain`, `langchain-community`, `chromadb`, `pypdf`, `openai`, `sentence-transformers`.
2. Drop a few real PDFs into `data/raw/`.
3. `ingest.py`: load → recursive character split (chunk=800, overlap=120) → embed → upsert to Chroma at `./chroma_db/`. Store `source` and `page` in metadata.
4. `ask.py`: take a question → embed → top-k (k=5) from Chroma → build a prompt that includes chunks with their source/page → call your `shared.llm_clients.chat()` → print answer + citations.
5. Write 10 Q&A pairs in `evals/qa.jsonl` (you write both Q and the chunk you expect retrieved).
6. `evals/run.py`: for each Q, check whether the expected chunk appears in the top-5. Print recall@5.
7. Swap the embedding model (OpenAI ↔ BGE) and re-run evals. Document the difference.

---

## What "done" looks like

- `python ask.py "What does the manual say about cooling thresholds?"` returns a useful answer with the right `[source: ... p.X]` tag.
- Recall@5 ≥ 0.7 on your eval set with either embedding model.
- You can clearly state two situations where this naive RAG breaks.

---

## Stretch

- Add metadata filters (e.g. answer only from a specific PDF or date range).
- Persist Chroma across runs and add an upsert key so re-ingesting doesn't duplicate.
- Try pgvector via Docker instead of Chroma — same API surface in LangChain.

---

## Production angle

You'll feel three real problems: (1) bad chunking destroys answers, (2) one-shot top-k retrieval misses things, (3) you have no idea if a system change made retrieval better or worse. Module 03 attacks all three.
