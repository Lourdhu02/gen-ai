# Gen-AI: Production-Grade LLM Engineering

A project-driven course. You learn by **building** — every module ships a working app. Minimal reading. Maximum hands-on.

> Audience: Python-comfortable engineer who's called LLM APIs before and wants to ship production-grade Gen-AI systems.

---

## How this course works

- **One folder per project.** Each has its own `venv`, `requirements.txt`, `.env.example`, code, and a short README.
- **VS Code first.** All work is done locally in VS Code; Colab is used only when a GPU is actually needed (fine-tuning, heavy local inference).
- **Multi-provider.** You'll write code against Claude, OpenAI, and open-source models (Ollama / Hugging Face). Provider-agnostic from day one.
- **Production lens.** Every project ends with the question: *what would break this in production?* — and we fix at least one thing.
- **No essays.** READMEs are short: goal, deliverable, key concepts, reference links, and a numbered task list. You learn by writing code, not reading mine.

---

## Setup (one time)

See [`SETUP.md`](./SETUP.md). Install Python 3.11+, VS Code + extensions, Docker, and get API keys for Anthropic + OpenAI + a free Colab account.

---

## The Roadmap

| # | Module | What you ship | GPU? |
|---|---|---|---|
| 00 | [Foundations](./00-foundations/) | Multi-provider hello-world: Claude + OpenAI + Ollama (local OSS) | No |
| 01 | [Prompt Playground + Evals](./01-prompt-playground/) | CLI tool to A/B prompts across providers with a basic eval harness | No |
| 02 | [RAG over Your Docs](./02-rag-basics/) | Chat-with-PDFs app — ingestion → chunking → embeddings → vector DB → answer with citations | No |
| 03 | [Advanced RAG](./03-rag-advanced/) | Hybrid search + reranking + query rewriting, evaluated with RAGAS | No |
| 04 | [Tool-Use Agent](./04-agent-tools/) | Agent that uses tools (web search, code exec, file ops) with guardrails | No |
| 05 | [Multi-Agent System](./05-multi-agent/) | Planner → workers → critic loop. LangGraph or custom orchestration | No |
| 06 | [Fine-tune on Colab](./06-finetune-colab/) | LoRA/QLoRA a small open model on a domain dataset, push to HF Hub | **Yes (Colab)** |
| 07 | [Multimodal](./07-multimodal/) | Document understanding / vision pipeline (e.g., screenshot → structured data) | Optional |
| 08 | [Capstone A: Productionize](./08-capstone-productionize/) | Take one earlier project → FastAPI + Docker + observability + cost controls | No |
| 09 | [Capstone B: Greenfield App](./09-capstone-greenfield/) | A new end-to-end app combining RAG + agents + (optional) fine-tuned model | Optional |

**Suggested pace (3–6 months):** 1–2 weeks per module 00–05, 2–3 weeks for 06–07, 3–4 weeks per capstone. Adjust freely.

---

## What you'll have at the end

- 10 working projects pushed to your GitHub (portfolio).
- One deployed app (Capstone A) running behind FastAPI in Docker with metrics + cost tracking.
- A reusable mental model: when to use prompts vs. fine-tuning vs. RAG vs. agents; when to swap models; how to evaluate any LLM system.
- Comfort with: Claude SDK, OpenAI SDK, Hugging Face, LangChain (where it helps), LangGraph, Ollama, vLLM (intro), pgvector/Chroma, RAGAS, Langfuse, FastAPI, Docker.

---

## Conventions

- **Each project is self-contained.** `cd 02-rag-basics && python -m venv .venv && ...`. No global mess.
- **Secrets via `.env`.** Never commit. Every project has `.env.example`.
- **Notebooks only where they help.** Most code is `.py` files run from VS Code. Notebooks are reserved for exploration (`notebooks/`) or Colab-required GPU work (`colab/`).
- **Shared code in `shared/`** — once we build a multi-provider LLM client in module 01, every later project imports it.
- **Reference links over reading.** Each README links to canonical docs; we don't re-explain them.

---

## How to start

1. Finish [`SETUP.md`](./SETUP.md).
2. Open [`00-foundations/README.md`](./00-foundations/) and run the three warm-up scripts.
3. Move to module 01.

That's it. Build.
