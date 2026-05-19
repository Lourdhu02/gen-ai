# Module 06 — Fine-tune on Colab GPU

**Goal:** LoRA / QLoRA fine-tune a small open model on your own dataset using a free Colab T4 GPU. Push it to the Hugging Face Hub. Serve it from local Ollama.

This is the first GPU-heavy module. Everything else has been CPU-friendly.

---

## What you'll ship

- `local/dataset_prep.py` — turns a raw dataset (CSV/JSONL) into the chat-format JSONL the trainer expects. Done locally in VS Code.
- `colab/finetune_qlora.ipynb` — runs on Colab T4. QLoRA fine-tunes `Qwen/Qwen2.5-1.5B-Instruct` (or similar small model) on your dataset.
- `colab/push_to_hub.ipynb` — merges LoRA adapters and pushes to `your-username/your-model-name` on HF Hub.
- `local/serve_with_ollama.md` — short notes on converting to GGUF and running with Ollama. (Or just download the HF model and run via `transformers`.)
- A simple before/after eval: 10 prompts, score base vs fine-tuned.

---

## Key concepts

- **LoRA / QLoRA** — train small adapter matrices instead of all weights. QLoRA also quantizes the base model to 4-bit so it fits on a free GPU.
- **Chat templates** — the exact tokenization format the model expects during training (`<|user|>...<|assistant|>...`). Get this wrong and nothing works.
- **PEFT** — Hugging Face library that implements LoRA cleanly.
- **TRL `SFTTrainer`** — the supervised fine-tuning trainer; handles the chat template and loss masking.
- **When to fine-tune vs prompt vs RAG**: fine-tune when you need *style/format* or to teach a *new behavior* the model can't be prompted into. Don't fine-tune to inject facts — that's RAG's job.

---

## Reference links

- HF PEFT: https://huggingface.co/docs/peft/index
- HF TRL: https://huggingface.co/docs/trl/index
- Qwen2.5 models: https://huggingface.co/Qwen
- "QLoRA" paper: https://arxiv.org/abs/2305.14314
- Unsloth (faster QLoRA on Colab): https://github.com/unslothai/unsloth
- HF model push: https://huggingface.co/docs/transformers/model_sharing

---

## Steps

### Locally (VS Code)

1. Pick a task with a clearly improvable signal. Examples:
   - **Style transfer**: turn formal text into bullet-point summaries.
   - **Structured extraction**: turn an email into a JSON support ticket.
   - **Domain Q&A**: answer questions in your team's voice.
2. Build a small dataset (200–1000 examples). Each: `{"messages": [{"role":"user","content":...},{"role":"assistant","content":...}]}`.
3. Split 90/10 train/val. Save to `local/data/{train,val}.jsonl`.
4. Sanity check: print 3 random examples to make sure the format is right.

### On Colab

5. Open `colab/finetune_qlora.ipynb` in Colab. Set Runtime → T4 GPU.
6. Mount Drive, upload `train.jsonl` and `val.jsonl`.
7. Run cells: load base model in 4-bit (bnb) → attach LoRA adapter (PEFT) → `SFTTrainer` for ~1–3 epochs → log to wandb or just prints.
8. Save adapters to Drive. Open `push_to_hub.ipynb` → log in with `HF_TOKEN` → merge + push.

### Back locally

9. Pull the model: `huggingface-cli download your-username/your-model-name`.
10. Run 10 eval prompts against base and fine-tuned. Write the comparison.

---

## What "done" looks like

- A model card on your HF Hub profile.
- A side-by-side eval doc showing the fine-tuned model clearly winning on the chosen task (or you've documented why it didn't and what to change).
- You can explain the chat template you used and why it matters.

---

## Stretch

- Try Unsloth — typically 2× faster QLoRA on the same Colab GPU.
- Convert your model to **GGUF** with `llama.cpp` and run it locally via `ollama create`.
- Run a DPO/ORPO preference-tuning pass on top of your SFT model with a small preference dataset.

---

## Production angle

In a real org, fine-tuning is the *last* thing you reach for — after prompting and RAG fail to hit the bar. But when you need consistent format, brand voice, or a behavior the base model fights, nothing else works as well. Knowing the actual mechanics — chat templates, LoRA, adapter merging — is what makes you employable here.
