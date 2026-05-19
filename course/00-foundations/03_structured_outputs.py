"""
Same prompt across all three providers, but each must return JSON
that matches a Pydantic schema. This is how real apps consume LLM output.

Approach per provider:
  - Claude:  tool use ("function calling") to force a schema-shaped response.
  - OpenAI:  response_format with the Pydantic model (Structured Outputs).
  - Ollama:  JSON mode + prompt instruction.

Run:  python 03_structured_outputs.py
"""

import json
import os

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

load_dotenv()
console = Console()


# ---------- The schema we want every provider to return ----------

class TechExplainer(BaseModel):
    term: str = Field(..., description="The technical term being explained")
    one_line: str = Field(..., description="A single-sentence definition")
    when_to_use: list[str] = Field(..., description="3 short bullet points: when this approach fits")
    when_not_to_use: list[str] = Field(..., description="3 short bullet points: when it does not fit")


PROMPT = "Explain RAG (Retrieval-Augmented Generation) using the given schema."


# ---------- Provider implementations ----------

def ask_claude_structured(prompt: str) -> TechExplainer:
    """Claude uses tool use to enforce structure."""
    import anthropic

    client = anthropic.Anthropic()
    schema = TechExplainer.model_json_schema()

    tool = {
        "name": "return_explanation",
        "description": "Return the technical explanation in the required schema.",
        "input_schema": schema,
    }

    msg = client.messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-haiku-4-5-20251001"),
        max_tokens=500,
        tools=[tool],
        tool_choice={"type": "tool", "name": "return_explanation"},
        messages=[{"role": "user", "content": prompt}],
    )

    for block in msg.content:
        if block.type == "tool_use":
            return TechExplainer.model_validate(block.input)
    raise RuntimeError("Claude did not return a tool_use block")


def ask_openai_structured(prompt: str) -> TechExplainer:
    """OpenAI: Structured Outputs (response_format=Pydantic model)."""
    from openai import OpenAI

    client = OpenAI()
    resp = client.beta.chat.completions.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        messages=[{"role": "user", "content": prompt}],
        response_format=TechExplainer,
    )
    parsed = resp.choices[0].message.parsed
    if parsed is None:
        raise RuntimeError("OpenAI returned no parsed object")
    return parsed


def ask_ollama_structured(prompt: str) -> TechExplainer:
    """Ollama: JSON mode + schema-in-prompt. Smaller models need both."""
    import ollama

    schema = TechExplainer.model_json_schema()
    system = (
        "You return only valid JSON matching this JSON Schema. No prose, no markdown. "
        "Schema: " + json.dumps(schema)
    )

    client = ollama.Client(host=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    resp = client.chat(
        model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        format="json",
        options={"temperature": 0.2, "num_predict": 500},
    )

    raw = resp["message"]["content"]
    data = json.loads(raw)
    return TechExplainer.model_validate(data)


# ---------- Run ----------

def main() -> None:
    console.print(Panel(PROMPT, title="Prompt", style="cyan"))

    providers = [
        ("claude", ask_claude_structured),
        ("openai", ask_openai_structured),
        ("ollama", ask_ollama_structured),
    ]

    for name, fn in providers:
        try:
            obj = fn(PROMPT)
            pretty = json.dumps(obj.model_dump(), indent=2)
            console.print(Panel(pretty, title=f"[bold]{name}[/bold]", border_style="green"))
        except Exception as e:
            console.print(
                Panel(f"{type(e).__name__}: {e}", title=f"[bold]{name}[/bold] (error)", border_style="red")
            )


if __name__ == "__main__":
    main()
