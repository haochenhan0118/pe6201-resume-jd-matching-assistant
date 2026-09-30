"""PII redaction and OpenAI-backed semantic resume matching."""

from __future__ import annotations

import os
from pathlib import Path
import re
from typing import Literal

from dotenv import load_dotenv
from pydantic import BaseModel, Field


PROJECT_DIR = Path(__file__).resolve().parent
load_dotenv(PROJECT_DIR / ".env")


class MatchResult(BaseModel):
    verdict: Literal["MATCH", "NO_MATCH", "MANUAL_REVIEW"]
    score: int = Field(ge=0, le=100)
    strengths: list[str] = Field(max_length=2)
    gaps: list[str] = Field(max_length=2)
    evidence: list[str] = Field(max_length=4)


def redact_pii(text: str) -> str:
    """Remove common direct identifiers before text is sent to an API."""
    redacted = re.sub(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "[EMAIL REDACTED]",
        text,
        flags=re.IGNORECASE,
    )
    redacted = re.sub(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
        "[PHONE REDACTED]",
        redacted,
    )

    lines = redacted.splitlines()
    for index, line in enumerate(lines[:3]):
        stripped = line.strip()
        if (
            stripped
            and len(stripped.split()) in {2, 3}
            and all(part.replace("-", "").isalpha() for part in stripped.split())
            and not any(char in stripped for char in ":|,@")
        ):
            lines[index] = "[NAME REDACTED]"
            break
    return "\n".join(lines)


def match_with_openai(job_description: str, resume: str) -> MatchResult:
    """Run one structured model call and return a validated result.

    OpenRouter is used when its key is configured. ``OPENAI_API_KEY`` remains a
    compatibility alias so an existing local .env file does not need to expose
    or rewrite its secret.
    """
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENROUTER_API_KEY is not configured. The keyword baseline still works."
        )

    from openai import OpenAI

    instructions = (PROJECT_DIR / "prompt.txt").read_text(encoding="utf-8")
    safe_resume = redact_pii(resume)
    is_openrouter = api_key.startswith("sk-or-") or bool(os.getenv("OPENROUTER_API_KEY"))
    user_content = (
        "Compare the following job description and resume.\n\n"
        "<job_description>\n"
        f"{job_description}\n"
        "</job_description>\n\n"
        "<resume>\n"
        f"{safe_resume}\n"
        "</resume>"
    )

    if is_openrouter:
        model = os.getenv("OPENROUTER_MODEL") or os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        if "/" not in model:
            model = f"openai/{model}"
        client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
        completion = client.chat.completions.parse(
            model=model,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_content},
            ],
            response_format=MatchResult,
        )
        parsed = completion.choices[0].message.parsed
    else:
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        client = OpenAI(api_key=api_key)
        response = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_content},
            ],
            text_format=MatchResult,
        )
        parsed = response.output_parsed

    if parsed is None:
        raise RuntimeError("The model did not return a structured result.")
    return parsed
