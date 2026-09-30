"""Minimal Streamlit interface for the PE6201 course project."""

from __future__ import annotations

import os

import streamlit as st

from baseline import keyword_match
from matcher import match_with_openai, redact_pii


DEFAULT_JD = """Junior Data Analyst

We are looking for a junior data analyst with practical Python, SQL, Excel,
statistics, and data visualization skills. The analyst will prepare reports,
build dashboards, and communicate findings to business stakeholders.
"""

DEFAULT_RESUME = """Alex Tan
alex.tan@example.com | +65 9123 4567

One year of experience preparing business reports with Python, SQL, Excel and
Tableau. Built weekly dashboards and presented findings to operations managers.
"""


st.set_page_config(page_title="Resume-JD Matching Assistant", page_icon="📄")
st.title("Resume-JD Matching Assistant")
st.caption("Course prototype: decision support only — never use it for automatic rejection.")

job_description = st.text_area("Job description", DEFAULT_JD, height=190)
resume = st.text_area("Resume", DEFAULT_RESUME, height=220)

with st.expander("Preview resume after local PII redaction"):
    st.code(redact_pii(resume), language=None)

baseline_tab, ai_tab = st.tabs(["Keyword baseline", "AI comparison"])

with baseline_tab:
    if st.button("Run keyword baseline", type="primary"):
        try:
            result = keyword_match(job_description, resume)
            st.metric("Keyword score", f"{result.score}%")
            st.write(f"**Decision-support label:** {result.verdict}")
            st.write("**Matched skills:**", ", ".join(result.matched_skills) or "None")
            st.write("**Missing skills:**", ", ".join(result.missing_skills) or "None")
        except ValueError as exc:
            st.error(str(exc))

with ai_tab:
    if not (os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")):
        st.info(
            "AI comparison is disabled until OPENROUTER_API_KEY is added to a local .env file. "
            "The key must never be committed to the repository."
        )

    if st.button("Run AI comparison"):
        try:
            with st.spinner("Comparing job-relevant evidence..."):
                result = match_with_openai(job_description, resume)
            st.metric("AI score", f"{result.score}%")
            st.write(f"**Decision-support label:** {result.verdict}")
            st.write("**Strengths**")
            for item in result.strengths:
                st.write(f"- {item}")
            st.write("**Gaps**")
            for item in result.gaps:
                st.write(f"- {item}")
            st.write("**Resume evidence**")
            for item in result.evidence:
                st.write(f"- {item}")
        except Exception as exc:
            st.error(f"AI comparison could not run: {exc}")

st.warning(
    "This prototype assists human review. It must not make hiring decisions or "
    "automatically reject a candidate."
)
