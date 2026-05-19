# Module 00 — Foundations

**Goal:** prove your laptop can talk to Claude, OpenAI, and a local open-source model. Then make all three return structured data.

If everything in this module runs, the rest of the course will run.

---

## What you'll ship

Three working Python scripts:

1. `01_check_env.py` — verifies Python, keys, and Ollama are reachable.
2. `02_first_calls.py` — sends the same prompt to Claude, OpenAI, and a local OSS model. Prints all three answers side-by-side.
3. `03_structured_outputs.py` — same idea, but each model must return valid JSON that matches a Pydantic schema.

---

## Key concepts (just enough)

- **API key auth** — every provider authenticates with a key in an env var. Never in code.
- **Provider SDKs** — `anthropic`, `openai`, `ollama` Python packages. Different shapes, same idea.
- **Structured outputs** — forcing the model to return JSON you can parse. Critical for production. We'll use Pydantic models + each provider's structured-output feature (tool use for Claude, `response_format` for OpenAI, JSON mode for Ollama).
- **Why a local OSS model?** Free, private, no rate limits during development. Slower and weaker than frontier models — that tradeoff is the whole game.

---

## Reference links

- Anthropic SDK (Python): https://docs.anthropic.com/en/api/client-sdks
- OpenAI SDK (Python): https://platform.openai.com/docs/libraries
- Ollama Python: https://github.com/ollama/ollama-python
- Pydantic: https://docs.pydantic.dev/latest/

---

## Steps

```powershell
# 1. From this folder
cd 00-foundations
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Copy env template and fill in keys
copy .env.example .env
# edit .env in VS Code, paste your ANTHROPIC_API_KEY and OPENAI_API_KEY

# 3. Make sure Ollama is running and has the model
ollama pull llama3.2:3b

# 4. Run the three scripts in order
python 01_check_env.py
python 02_first_calls.py
python 03_structured_outputs.py
```

Read each script before you run it. They're short on purpose.

---

## What "done" looks like

- `01_check_env.py` prints ✅ for all four checks (python version, anthropic key, openai key, ollama reachable).
- `02_first_calls.py` prints three answers labeled `[claude]`, `[openai]`, `[ollama]`.
- `03_structured_outputs.py` prints three Pydantic-validated objects with the same schema.

If any step fails, fix it before moving on. Each project after this assumes all three providers work.

---

## Stretch (optional)

- Add **streaming** to `02_first_calls.py` so each provider's tokens appear live. Check each SDK's streaming docs.
- Add a 4th provider (Google Gemini or Groq). See if your code stays clean or starts to smell — that pain motivates module 01.
- Time each call. Notice how local Ollama compares to API latency on a cold start vs warm.

---

## Production angle

In production you almost never call SDKs directly from app code. You wrap them. Notice how `02_first_calls.py` has three separate code paths — repetitive, brittle, and hard to test. **Module 01 fixes this** by building a unified client. You'll feel why before you build it.
