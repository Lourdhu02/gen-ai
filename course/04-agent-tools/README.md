# Module 04 — Tool-Use Agent

**Goal:** build an agent that decides which tool to call, calls it, reads the result, and loops until done. With safety rails so it doesn't burn through your budget or do something dumb.

---

## What you'll ship

- `agent.py` — a tool-use loop you wrote yourself (no LangChain wrapper yet). Supports: web search (Tavily), Python code execution (sandboxed), and local file read/write (scoped to a workspace dir).
- A budget guard: hard limit on iterations, tokens, and tool calls per session.
- A confirmation hook for "risky" tools (e.g. file write outside a whitelist).
- Two example sessions you save as transcripts: a "research a topic" run and a "fix this small bug in this script" run.

---

## Key concepts

- **The tool-use loop** — model returns either a final answer or `tool_use` blocks → you execute the tool → feed `tool_result` back → repeat.
- **Tool schemas** — JSON Schema describes each tool's params. The model picks parameters; you validate.
- **Stop conditions** — max steps, max tokens, max wall-clock, repeated identical tool calls.
- **Sandboxing** — code exec must NEVER hit your host directly. Use `subprocess` into a Docker container, or `restrictedpython`, or fail loud.
- **Guardrails** — prompt-injection awareness (treat tool outputs as untrusted), URL allowlist for fetch, path scoping for file tools.

---

## Reference links

- Anthropic tool use: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/overview
- OpenAI function calling: https://platform.openai.com/docs/guides/function-calling
- Tavily search: https://docs.tavily.com/
- Anthropic Claude Agent SDK: https://docs.anthropic.com/en/api/agent-sdk/overview
- "Building effective agents" — Anthropic: https://www.anthropic.com/research/building-effective-agents

---

## Steps

1. Define the tools as JSON-Schema dicts: `web_search(query)`, `read_file(path)`, `write_file(path, content)`, `run_python(code)`.
2. Implement Python handlers for each. `run_python` must run in a Docker container (`docker run --rm python:3.11-slim`) with no network and a timeout. Start simple, harden after it works.
3. Write the loop: call model with `tools=…` → if `tool_use` blocks, execute, append `tool_result`, loop. If `end_turn`, return.
4. Add budget guard: counters for iterations, total tokens, tool calls. Raise once exceeded.
5. Add a confirm hook: before calling any "writing" tool, print plan + ask for `y/n`. (Make it toggleable.)
6. Run the "research" session: ask the agent to research a recent paper and write a 5-bullet summary to `out/notes.md`.
7. Run the "fix bug" session: drop a broken Python file into the workspace, ask the agent to fix it. Watch the transcript.

---

## What "done" looks like

- The agent completes both sessions without exceeding budget.
- Tool-call transcripts are saved and human-readable.
- Killing Docker mid-run doesn't corrupt your workspace.

---

## Stretch

- Add an MCP server with your tools instead of inline JSON Schema; connect via Claude Agent SDK.
- Add a "reflection" step: after each tool result, the agent writes one line to a scratchpad before deciding the next action.
- Add a per-tool retry policy with exponential backoff.

---

## Production angle

Real agents fail in three ways: (1) they loop forever, (2) they call expensive tools too eagerly, (3) they get prompt-injected by tool output. Your guardrails this module are the minimum viable defense.
