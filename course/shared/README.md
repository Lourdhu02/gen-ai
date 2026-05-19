# `shared/` — code reused across projects

This folder stays empty until **module 01**, where we build a multi-provider LLM client (`llm_clients.py`) that all later projects import.

## Why `shared/`?

After module 01 you'll have a unified interface for calling Claude / OpenAI / Ollama with one function. Instead of copying it into every project, projects 02–09 will install it as a local editable package or import it via `PYTHONPATH`.

## Setup pattern (introduced in module 01)

Each downstream project will have either:

```powershell
# from inside a project venv
pip install -e ../shared
```

…or a `conftest.py` / `sys.path` shim. We'll cover the simplest of these in module 01.

For now: leave it alone.
