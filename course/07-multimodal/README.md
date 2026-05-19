# Module 07 — Multimodal

**Goal:** build a vision-text pipeline. Pick one: "screenshot → structured data" or "PDF/document understanding." Ship something that actually works on messy real-world images.

---

## What you'll ship (pick one project)

### Option A — Screenshot to Structured Data
- Input: a screenshot (a receipt, a UI mockup, an invoice, a chart).
- Output: typed structured data (`InvoiceLine[]`, `ChartData`, `UIComponentTree`, …).
- Validated with Pydantic.

### Option B — Document Understanding Pipeline
- Input: a multi-page PDF (scanned or born-digital).
- Output: structured content — tables extracted as JSON, figures captioned, sections labeled.
- Combines OCR (if needed) + vision LLM.

Both options ship: a CLI + an eval set of ~20 hand-labeled examples + a results table comparing 2–3 vision models.

---

## Key concepts

- **Vision-capable models** — Claude (Sonnet/Opus), GPT-4o, Gemini, Qwen2-VL (OSS, runs on bigger GPUs).
- **Image encoding** — base64 vs URL; size limits per provider; image-token cost.
- **OCR fallback** — vision LLMs are NOT OCR; for dense scanned docs use Tesseract or `docTR` first, then feed text + image to the LLM.
- **Grounded output** — same idea as RAG: force JSON schema, validate, retry on failure.
- **Eval for vision** — exact-match on extracted fields; field-level F1 for structured output.

---

## Reference links

- Anthropic vision: https://docs.anthropic.com/en/docs/build-with-claude/vision
- OpenAI vision: https://platform.openai.com/docs/guides/vision
- Qwen2-VL: https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct
- Tesseract: https://github.com/tesseract-ocr/tesseract
- docTR: https://github.com/mindee/doctr
- "Unstructured" library (PDF parsing): https://github.com/Unstructured-IO/unstructured

---

## Steps (using Option A as the example)

1. Collect 20 real screenshots for your chosen task. Hand-label the expected JSON output.
2. Define the Pydantic schema for the output.
3. Build `extract.py` — loads image, base64-encodes, calls vision LLM with schema-as-tool, validates output.
4. Add retry-with-feedback: if Pydantic validation fails, send the error message back to the model and retry once.
5. Run on all 20 examples; compute field-level accuracy. Save outputs to `runs/`.
6. Swap to a second vision model (e.g. Claude Sonnet ↔ GPT-4o). Compare.
7. Note failure modes: small text? overlapping elements? unusual layouts? Write them down — they're your moat.

---

## What "done" looks like

- Pipeline succeeds on ≥ 70% of real examples with valid schema.
- Eval doc compares ≥ 2 models with cost + accuracy.
- You can name the failure modes by image type.

---

## Stretch

- Add a local Qwen2-VL run via Hugging Face `transformers` (needs ~16GB VRAM — Colab Pro or A100 spot).
- Combine with module 02: RAG over the extracted structured data ("find every invoice over $5k from 2025").
- Add layout-aware OCR (`docTR`) and use bounding boxes to highlight extracted regions in the original image.

---

## Production angle

Vision-LLM pipelines are how most "AI document automation" startups make money right now. The hard part isn't the model call — it's the eval set, the schema, and the retry logic. You're building exactly those.
