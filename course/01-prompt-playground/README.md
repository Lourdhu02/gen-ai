# Module 01 — Prompt Playground + Evals

**Goal:** stop copy-pasting provider code. Build the unified LLM client you'll use for the rest of the course, plus a CLI playground for A/B-testing prompts and a basic eval harness.

---

## What you'll ship

- `shared/llm_clients.py` — one `chat(provider, model, messages, **kwargs)` function that wraps Claude, OpenAI, and Ollama. Imported by every later project.
- `playground.py` — CLI: take a prompt file + a list of providers/models, run them all, show outputs side-by-side, save to JSONL.
- `evals/run_evals.py` — runs a small eval set (10–20 cases) across multiple models, scores with a judge model, prints a comparison table.

---

## Key concepts

- **Provider abstraction** — a single internal `Message` and `LLMResponse` shape; per-provider adapters convert in/out.
- **Prompt versioning** — store prompts as `.md` or `.yaml` files with versions. Never inline-edit production prompts.
- **Golden-set evals** — `(input, expected)` pairs scored by either an exact-match rule, a Pydantic schema, or an LLM-as-judge.
- **LLM-as-judge** — using a strong model (e.g. Claude Opus / GPT-4o) to grade weaker models' outputs. Cheap, biased, useful when calibrated.
- **Cost & latency tracking** — log tokens in/out and wall time per call. You'll need this every project after.

---

## Reference links

- Anthropic — messages: https://docs.anthropic.com/en/api/messages
- OpenAI — chat completions: https://platform.openai.com/docs/api-reference/chat
- Pydantic v2: https://docs.pydantic.dev/latest/
- Promptfoo (inspiration for the eval harness): https://www.promptfoo.dev/docs/intro/
- "Your AI product needs evals" — Hamel Husain: https://hamel.dev/blog/posts/evals/

---

## Steps

1. Create the project: `cd 01-prompt-playground && python -m venv .venv && activate && pip install -r requirements.txt`.
2. In `shared/`, define `Message`, `LLMResponse` (with `text`, `tokens_in`, `tokens_out`, `latency_ms`, `cost_usd`), and a `chat()` dispatcher.
3. Implement three adapters: `_chat_anthropic`, `_chat_openai`, `_chat_ollama`. Map errors to a single `LLMError` exception.
4. Wire prompts as files in `prompts/` (one per task, frontmatter for version + description).
5. Build `playground.py` with [`typer`](https://typer.tiangolo.com/) or `argparse`: `--prompt`, `--providers`, `--n` (repeats).
6. Build `evals/dataset.jsonl` with 10–20 cases for one chosen task (e.g. "summarize this email in 3 bullets").
7. Build `evals/run_evals.py` — runs each case across N models, scores via LLM-as-judge, prints a table (rich), writes results to `evals/runs/<timestamp>.jsonl`.
8. Run it on Haiku vs gpt-4o-mini vs llama3.2:3b. Eyeball whether the judge agrees with you on a few cases.

---

## What "done" looks like

- `from shared.llm_clients import chat` works from any sibling project.
- `python playground.py --prompt prompts/summarize_email.md --providers claude,openai,ollama` prints 3 panels.
- `python evals/run_evals.py` outputs a comparison table with cost per model and judge scores per case.

---

## Stretch

- Add prompt caching for Claude (the `cache_control` block) and measure the cost delta on the eval run.
- Add `--stream` to the playground.
- Compute inter-judge agreement: run two different judge models, measure Cohen's kappa.

---

## Production angle

This module is the foundation of every serious LLM app. In prod you'll have: versioned prompts in source control, a CI step that runs your eval set on every PR, alerts when win-rate drops. You're building that pipeline in miniature.
