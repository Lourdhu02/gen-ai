# Module 09 — Capstone B: Greenfield End-to-End App

**Goal:** combine everything. A brand-new app that uses RAG + agents + (optionally) your fine-tuned model + multimodal. Ship a small product, not a notebook.

---

## What you'll ship

A real Gen-AI product you'd actually use. You scope it. Examples that combine multiple modules well:

- **"AI second-brain"** — ingests your notes, PDFs, web bookmarks (RAG); a chat UI; an agent that can also write/edit notes (tool use); multimodal (paste screenshots → OCR + tag).
- **"Recruiter assistant"** — RAG over JDs and resumes; agent that drafts personalized outreach; structured extraction from PDFs (multimodal); fine-tuned model on your writing style (M06).
- **"Codebase reviewer"** — RAG over a repo; agent that opens files, runs tests, proposes patches; LangGraph workflow (planner → fixer → critic).
- **Your idea** — even better.

Plus: a simple frontend (Streamlit or Next.js minimal), deployed.

---

## Constraints (this is the point of the capstone)

- Must integrate **at least 3** of: RAG, agents, multi-agent, fine-tuned model, multimodal.
- Must have **evals** — a small golden set you run before each deploy.
- Must have **observability** — Langfuse traces on every LLM call.
- Must be **cost-aware** — log spend per session; cap per user.
- Must be **deployed** — a real URL.

---

## Reference links

- Streamlit: https://docs.streamlit.io/
- Next.js: https://nextjs.org/docs
- Vercel AI SDK (if Next): https://sdk.vercel.ai/
- Modal (alternative to Fly.io, GPU-friendly): https://modal.com/docs

---

## Steps

1. **Scope ruthlessly.** Pick ONE user persona, ONE primary job-to-be-done. Write a one-page brief: who, what, success metric.
2. **Prototype the LLM logic** as scripts before you build any UI. Use module 01–07 patterns.
3. **Define the eval set** before you finish. 20 cases minimum. Run them now to set baseline.
4. **Build the API** (FastAPI, like M08).
5. **Build the minimum UI** — Streamlit is fastest if you don't care about polish; Next.js if you do.
6. **Deploy.** Same flow as M08.
7. **Run evals on the deployed system.** Compare to baseline.
8. **Demo it to someone.** Get one piece of feedback. Fix the most painful thing they hit.

---

## What "done" looks like

- A URL you can show.
- A README that pitches the product in one paragraph and explains the architecture.
- An evals doc showing pre/post deployment performance.
- A 2-minute demo video (Loom or similar).

---

## Stretch

- Open source it. Write a launch blog post.
- Add billing (Stripe).
- Replace one paid model call with your fine-tuned local model and document the cost savings.

---

## Production angle

You're now an engineer who has built and shipped a Gen-AI product end-to-end, with evals, observability, and cost controls. Most "AI engineers" online have built a notebook. You've built a system.
