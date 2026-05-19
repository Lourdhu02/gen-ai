# Setup (one time)

Do this once. After this, every project just needs its own `venv` + `pip install -r requirements.txt`.

---

## 1. Python 3.11+

Verify:
```powershell
python --version
```
If missing or older than 3.11, install from https://www.python.org/downloads/. Check "Add Python to PATH" during install.

Make sure `pip` is current:
```powershell
python -m pip install --upgrade pip
```

---

## 2. VS Code + extensions

Install VS Code: https://code.visualstudio.com/

Extensions (install via the Extensions panel or `code --install-extension <id>`):

| Extension | Why |
|---|---|
| `ms-python.python` | Python language support, venv detection, debugging |
| `ms-python.vscode-pylance` | Fast type checker / IntelliSense |
| `ms-toolsai.jupyter` | Run `.ipynb` notebooks inside VS Code |
| `ms-azuretools.vscode-docker` | Manage Docker containers (needed from Capstone A) |
| `tamasfe.even-better-toml` | Read `pyproject.toml` / dependency files cleanly |
| `humao.rest-client` | Hit your FastAPI endpoints from VS Code |

Optional but recommended: `GitHub.copilot` or your AI assistant of choice — but try to write the code yourself first.

---

## 3. Per-project venv pattern

Every project in this course follows this exact pattern. Memorize it:

```powershell
cd 00-foundations
python -m venv .venv
.\.venv\Scripts\Activate.ps1          # PowerShell
# or: .\.venv\Scripts\activate.bat    # cmd
pip install -r requirements.txt
```

In VS Code, when you open a project folder, it should auto-detect the `.venv`. If not:
- `Ctrl+Shift+P` → **Python: Select Interpreter** → pick the one inside `.venv`.

To leave the venv: `deactivate`.

> **Why one venv per project?** Dependencies conflict fast in Gen-AI (different `torch` versions, different `langchain` versions, etc.). Isolation saves you hours.

---

## 4. API keys — get them now

You'll need these. Store them in each project's `.env` file (never commit).

| Provider | Where to get | Free tier? |
|---|---|---|
| Anthropic (Claude) | https://console.anthropic.com/ → API Keys | $5 free credit on signup |
| OpenAI | https://platform.openai.com/api-keys | Pay-as-you-go |
| Hugging Face | https://huggingface.co/settings/tokens | Free (needed for model downloads + Hub push in module 06) |
| Tavily (web search for agent) | https://tavily.com/ | 1000 free calls/month |
| Langfuse (observability) | https://cloud.langfuse.com/ | Free tier — sign up later, used from module 03 |

Create one master `.env` file for yourself (NOT in the course folder — somewhere safe like `D:\Lourdu-Personal\.secrets\genai.env`) so you can copy values into each project's `.env` as needed.

Example master file:
```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
HF_TOKEN=hf_...
TAVILY_API_KEY=tvly-...
LANGFUSE_PUBLIC_KEY=pk-...
LANGFUSE_SECRET_KEY=sk-...
```

---

## 5. Ollama (local OSS models, no GPU needed)

For running open-source models locally on CPU/GPU. Used from module 00 onward.

Install: https://ollama.com/download → run installer → it adds `ollama` to PATH.

Pull a small model to test:
```powershell
ollama pull llama3.2:3b
ollama run llama3.2:3b "Say hi in one sentence."
```

`llama3.2:3b` runs on most laptops. We'll use bigger ones (`qwen2.5:7b`, `llama3.1:8b`) when your machine can handle it, and Colab for anything larger.

---

## 6. Docker (needed from Capstone A onward)

Install Docker Desktop: https://www.docker.com/products/docker-desktop/

Verify:
```powershell
docker --version
docker run hello-world
```

---

## 7. Google Colab + GPU (needed from module 06)

- Sign in at https://colab.research.google.com/ with a Google account.
- Open any notebook → **Runtime** → **Change runtime type** → **T4 GPU** (free tier).
- Connect your Google Drive (in module 06 we mount it to save model checkpoints).

**Workflow we'll use:** write code locally in VS Code → push notebook to `06-finetune-colab/colab/` → open it in Colab via "Open in Colab" or upload → run the training there → pull artifacts back.

VS Code can also tunnel into a Colab GPU runtime (advanced), but the simpler push-notebook flow is what we'll teach.

---

## 8. Git + GitHub

You'll push every project. If not set up:

```powershell
git --version
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Create a private GitHub repo: `gen-ai-course` (or however you name it). We'll `git init` inside `course/` later.

---

## 9. Verify the setup

Open the `00-foundations/` folder in VS Code and follow its README. The three scripts there are the smoke test for this entire setup.

---

## Troubleshooting

- **`Activate.ps1` blocked**: PowerShell execution policy. Run once as your user:
  `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`
- **`ollama` not found**: restart your terminal after installing.
- **`pip install` SSL errors**: corporate proxy or outdated certs. Try `pip install --upgrade certifi`.
- **VS Code doesn't see the venv**: close & reopen the folder, then `Python: Select Interpreter`.
