"""Transparent keyword-overlap baseline for the course comparison."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import re


SKILL_ALIASES: dict[str, tuple[str, ...]] = {
    "python": ("python",),
    "sql": ("sql", "mysql", "postgresql", "postgres", "sqlite"),
    "excel": ("excel", "spreadsheet", "spreadsheets"),
    "tableau": ("tableau",),
    "power bi": ("power bi", "powerbi"),
    "statistics": ("statistics", "statistical analysis"),
    "data visualization": ("data visualization", "data visualisation", "dashboarding"),
    "pandas": ("pandas",),
    "numpy": ("numpy",),
    "machine learning": ("machine learning",),
    "communication": ("communication", "stakeholder communication"),
}


@dataclass(frozen=True)
class BaselineResult:
    verdict: str
    score: int
    required_skills: list[str]
    matched_skills: list[str]
    missing_skills: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def _contains_phrase(text: str, phrase: str) -> bool:
    pattern = rf"(?<!\w){re.escape(phrase.lower())}(?!\w)"
    return re.search(pattern, text.lower()) is not None


def extract_skills(text: str) -> list[str]:
    """Return canonical skills found in text using a fixed vocabulary."""
    found: list[str] = []
    for canonical, aliases in SKILL_ALIASES.items():
        if any(_contains_phrase(text, alias) for alias in aliases):
            found.append(canonical)
    return found


def keyword_match(job_description: str, resume: str) -> BaselineResult:
    required = extract_skills(job_description)
    if not required:
        raise ValueError(
            "No supported skills were found in the job description. "
            "Add at least one skill from the baseline vocabulary."
        )

    resume_skills = set(extract_skills(resume))
    matched = [skill for skill in required if skill in resume_skills]
    missing = [skill for skill in required if skill not in resume_skills]
    score = round(100 * len(matched) / len(required))

    if score >= 70:
        verdict = "MATCH"
    elif score >= 50:
        verdict = "MANUAL_REVIEW"
    else:
        verdict = "NO_MATCH"

    return BaselineResult(
        verdict=verdict,
        score=score,
        required_skills=required,
        matched_skills=matched,
        missing_skills=missing,
    )

