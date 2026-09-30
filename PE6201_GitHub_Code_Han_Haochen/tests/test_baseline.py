import pytest

from baseline import keyword_match


def test_keyword_match_returns_expected_overlap():
    result = keyword_match(
        "The role requires Python, SQL, Excel, Tableau and statistics.",
        "Used Python, SQL and Excel to produce reports.",
    )

    assert result.score == 60
    assert result.verdict == "MANUAL_REVIEW"
    assert result.matched_skills == ["python", "sql", "excel"]
    assert result.missing_skills == ["tableau", "statistics"]


def test_keyword_match_requires_known_skill():
    with pytest.raises(ValueError):
        keyword_match("Friendly office role.", "General office experience.")

