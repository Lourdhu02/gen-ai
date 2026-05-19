"""
Sends the same prompt to Claude, OpenAI, and a local Ollama model.
Prints each response side-by-side.

Notice the duplication across providers. Module 01 will unify this.

Run:  python 02_first_calls.py
"""

import os

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()

PROMPT = "In one sentence, what is the difference between fine-tuning and RAG?"


def ask_claude(prompt: str) -> str:
    import anthropic

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    msg = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    # Claude returns a list of content blocks; we want the text from the first.
    return msg.content[0].text.strip()


def ask_openai(prompt: str) -> str:
    from openai import OpenAI

    client = OpenAI()  # reads OPENAI_API_KEY
    resp = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return (resp.choices[0].message.content or "").strip()


def ask_ollama(prompt: str) -> str:
    import ollama

    client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    resp = client.chat(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        messages=[{"role": "user", "content": prompt}],
        options={"num_predict": 200},
    )
    return resp["message"]["content"].strip()


def main() -> None:
    console.print(Panel(PROMPT, title="Prompt", style="cyan"))

    providers = [
        ("claude", ask_claude),
        ("openai", ask_openai),
        ("ollama", ask_ollama),
    ]

    for name, fn in providers:
        try:
            answer = fn(PROMPT)
            console.print(Panel(answer, title=f"[bold]{name}[/bold]", border_style="green"))
        except Exception as e:
            console.print(Panel(f"{type(e).__name__}: {e}", title=f"[bold]{name}[/bold] (error)", border_style="red"))


if __name__ == "__main__":
    main()
