"""
Verifies that your environment is ready for the rest of the course.

Run:  python 01_check_env.py
"""

import os
import sys

from dotenv import load_dotenv
from rich.console import Console

console = Console()
load_dotenv()


def check(label: str, ok: bool, detail: str = "") -> bool:
    mark = "[green]OK[/green]" if ok else "[red]FAIL[/red]"
    console.print(f"[bold]{mark}[/bold]  {label}" + (f"  — {detail}" if detail else ""))
    return ok


def main() -> int:
    results = []

    # 1. Python version
    py_ok = sys.version_info >= (3, 11)
    results.append(check("Python >= 3.11", py_ok, f"got {sys.version.split()[0]}"))

    # 2. Anthropic key present and looks plausible
    anth = os.getenv("ANTHROPIC_API_KEY", "")
    results.append(
        check(
            "ANTHROPIC_API_KEY set",
            anth.startswith("sk-ant-") and len(anth) > 20,
            "set in .env" if anth.startswith("sk-ant-") else "missing or placeholder",
        )
    )

    # 3. OpenAI key present and looks plausible
    oai = os.getenv("OPENAI_API_KEY", "")
    results.append(
        check(
            "OPENAI_API_KEY set",
            oai.startswith("sk-") and "replace-me" not in oai,
            "set in .env" if oai.startswith("sk-") and "replace-me" not in oai else "missing or placeholder",
        )
    )

    # 4. Ollama reachable
    ollama_ok = False
    ollama_detail = ""
    try:
        import ollama

        client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
        models = client.list().get("models", [])
        ollama_ok = True
        ollama_detail = f"{len(models)} model(s) installed"
    except Exception as e:
        ollama_detail = f"{type(e).__name__}: {e}"
    results.append(check("Ollama reachable", ollama_ok, ollama_detail))

    console.print()
    if all(results):
        console.print("[bold green]All checks passed.[/bold green] You can run 02_first_calls.py next.")
        return 0
    else:
        console.print("[bold red]Fix the failures above before continuing.[/bold red]")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
