# Module 05 — Multi-Agent System

**Goal:** orchestrate multiple specialized agents — a planner, executor(s), and critic — using LangGraph. Build a research-and-write workflow that visibly outperforms a single agent.

---

## What you'll ship

- A LangGraph state machine: **Planner → Worker (loop) → Critic → either back to Worker or finalize**.
- Shared state object (TypedDict) that flows through nodes.
- A real task: "given a topic, produce a 500-word brief with 5 citations." Run it end-to-end.
- A comparison: same task with a single agent (module 04) vs the multi-agent system. Show quality + cost difference.

---

## Key concepts

- **State graphs** — nodes = functions, edges = transitions. State is explicit, not hidden in the conversation.
- **Planner/Executor/Critic** — separation of concerns. The planner doesn't execute; the critic doesn't write the final.
- **Conditional edges** — Critic decides: pass → finalize, fail → back to Worker with feedback (bounded retries).
- **Streaming intermediate state** — LangGraph supports streaming each node's output. Useful for UIs.
- **When NOT to use multi-agent** — it's slower and more expensive. Use it when the task has clearly distinct subtasks or needs review/critique.

---

## Reference links

- LangGraph: https://langchain-ai.github.io/langgraph/
- LangGraph tutorials: https://langchain-ai.github.io/langgraph/tutorials/
- "Multi-agent design patterns" — LangChain blog
- AutoGen (alternative framework): https://microsoft.github.io/autogen/

---

## Steps

1. Sketch the state: `{topic, plan, drafts, critique, final, iterations, tool_calls}`.
2. Implement nodes:
   - `plan` — LLM produces a 5-step plan as a list.
   - `worker` — executes the next step (uses web_search tool from M04).
   - `critic` — scores the draft on 3 axes (factuality, structure, completeness). Returns `accept | revise`.
   - `finalize` — packages output.
3. Wire conditional edges between worker → critic and critic → worker (with `iterations < max`).
4. Run the workflow; stream intermediate states to console with `rich`.
5. Run the same task with a single-tool agent. Compare: output quality (you judge), token cost, wall time.

---

## What "done" looks like

- LangGraph emits a clean state trace per run.
- The multi-agent run measurably beats the single-agent run on quality OR clearly does not — and you can articulate why.
- The system terminates cleanly on every input (no infinite loops).

---

## Stretch

- Add **memory** across runs (LangGraph's checkpointer with SQLite). Demonstrate resuming a paused workflow.
- Add a **human-in-the-loop** interrupt before finalize (LangGraph `interrupt_before`).
- Add **parallel workers** that each tackle a sub-task and a join node that merges.

---

## Production angle

Multi-agent in prod = pipelines. The reason to use LangGraph instead of writing your own loop is the checkpointing, streaming, and observability that comes free. You don't add complexity for free — you add it when the task can't be done well otherwise.
