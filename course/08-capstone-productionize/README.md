# Module 08 — Capstone A: Productionize One Earlier Project

**Goal:** pick your favorite earlier project (RAG, agent, or fine-tuned model service) and turn it into a real service. FastAPI + Docker + observability + cost controls + deploy.

This is the module that makes your portfolio look like an engineer's, not a tutorial-watcher's.

---

## What you'll ship

- `api/` — FastAPI service with: `/chat` (or `/ask`), `/health`, `/metrics`. Auth via API key header.
- `Dockerfile` — slim image, multi-stage, non-root user, < 1GB.
- `docker-compose.yml` — your service + Postgres (or pgvector) + Langfuse self-hosted.
- Observability: every LLM call logged to Langfuse with traces, costs, latency.
- Cost guard: per-key spend limit; circuit-breaker if monthly cap exceeded.
- Deployed somewhere public: Fly.io, Railway, or a small VM. Include a `DEPLOY.md`.
- A `loadtest/` folder with a `locust` script and a results screenshot.

---

## Key concepts

- **API as a contract** — request/response Pydantic models, OpenAPI auto-docs, versioned routes (`/v1/...`).
- **Streaming responses** — FastAPI `StreamingResponse` + SSE so clients see tokens as they arrive.
- **Observability** — every request gets a trace ID; every LLM call inside it is a span. You need to see why a slow request was slow.
- **Cost controls** — per-route token budget; auth-based daily limit; alarms before spend, not after.
- **Containerization** — slim base, deterministic deps, no secrets in image.
- **Stateless vs stateful** — RAG index in a volume, app stateless. Or use a managed vector store.

---

## Reference links

- FastAPI: https://fastapi.tiangolo.com/
- Langfuse self-hosted: https://langfuse.com/docs/deployment/self-host
- Docker multi-stage: https://docs.docker.com/build/building/multi-stage/
- Fly.io: https://fly.io/docs/
- Locust: https://docs.locust.io/

---

## Steps

1. Pick which project to productionize. Recommend: the RAG-advanced pipeline (M03) — most useful demo for portfolio.
2. Wrap your existing CLI as a FastAPI app. Define `ChatRequest`/`ChatResponse` Pydantic models.
3. Add auth: header `X-API-Key`. Store keys + per-key monthly cap in Postgres.
4. Add Langfuse tracing around every LLM call. Confirm traces show in the local Langfuse UI.
5. Add streaming endpoint `/v1/chat/stream` returning SSE.
6. Write the Dockerfile (multi-stage; final image based on `python:3.11-slim`). Test `docker compose up`.
7. Write the `locust` load test. Run it locally first. Tune workers.
8. Deploy: pick Fly.io (recommended) → `flyctl launch` → set secrets → `flyctl deploy`.
9. Hit the deployed URL with `curl` and the load test. Record metrics.

---

## What "done" looks like

- A public URL serving real LLM responses.
- A Langfuse dashboard showing your last 100 requests with costs.
- Load test surviving 10 RPS with reasonable p95 latency.
- A README anyone can follow to redeploy from scratch.

---

## Stretch

- Add Redis as a response cache (cache hits = $0).
- Add A/B routing: 10% of traffic hits a new prompt version; Langfuse measures win-rate.
- Add Prometheus + Grafana for infra metrics next to Langfuse for LLM metrics.

---

## Production angle

If you can demonstrate this module's app at a job interview, you have shipped production Gen-AI. Most candidates can't.
