"""Streamlit interface for the PE6201 resume matching course project.

The module keeps the demonstration deliberately small: one job description,
one resume, a transparent keyword baseline, and one optional structured LLM
call. Presentation logic lives here; matching, redaction, and evaluation logic
remain in separate modules so that each component can be reviewed independently.
"""

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


st.set_page_config(
    page_title="Resume-JD Review Assistant",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #10233f;
        --muted: #52657a;
        --blue: #2563a6;
        --line: #dbe5ef;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #f4f8fc 0%, #ffffff 34%);
    }
    [data-testid="stHeader"] { background: rgba(255,255,255,0.82); }
    .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
    .hero {
        padding: 2.1rem 2.3rem;
        border-radius: 22px;
        background: linear-gradient(125deg, #102f53 0%, #1e5c96 72%, #2c78b8 100%);
        color: white;
        box-shadow: 0 14px 34px rgba(16, 47, 83, 0.16);
        margin-bottom: 1.3rem;
    }
    .hero-badge {
        display: inline-block;
        padding: 0.28rem 0.68rem;
        border: 1px solid rgba(255,255,255,0.35);
        border-radius: 999px;
        font-size: 0.78rem;
        letter-spacing: 0.04em;
        margin-bottom: 0.85rem;
    }
    .hero h1 { color: white; font-size: 2.25rem; margin: 0 0 0.55rem 0; }
    .hero p { color: #e6f0fa; font-size: 1.03rem; max-width: 780px; margin: 0; }
    .section-kicker {
        color: var(--blue);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.15rem;
    }
    [data-testid="stMetric"] {
        background: rgba(255,255,255,0.92);
        border: 1px solid var(--line);
        padding: 1rem 1.1rem;
        border-radius: 15px;
        box-shadow: 0 5px 16px rgba(20, 52, 85, 0.06);
    }
    [data-testid="stTextArea"] textarea {
        border-radius: 12px;
        border-color: #cbd8e6;
        background: #fbfdff;
    }
    [data-testid="stButton"] button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 2.75rem;
    }
    [data-testid="stTabs"] [role="tablist"] { gap: 0.45rem; }
    [data-testid="stTabs"] button[role="tab"] {
        border-radius: 9px 9px 0 0;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .result-label {
        display: inline-block;
        padding: 0.3rem 0.65rem;
        border-radius: 999px;
        color: #12324f;
        background: #e7f1fa;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .footer-note {
        color: var(--muted);
        text-align: center;
        font-size: 0.82rem;
        margin-top: 2.2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.subheader("How to use this prototype")
    st.markdown(
        """
        1. Review or replace the sample texts.
        2. Preview the locally redacted resume.
        3. Run the transparent keyword baseline.
        4. Run the AI comparison when an API key is configured.
        """
    )
    st.divider()
    st.subheader("Decision boundary")
    st.info(
        "This tool supports human review. It must not automatically reject, "
        "rank, or hire a candidate."
    )
    st.subheader("Evaluation scope")
    st.caption(
        "Reported results use 40 held-out synthetic cases for one Junior Data "
        "Analyst role. They do not establish production hiring validity."
    )


st.markdown(
    """
    <div class="hero">
      <div class="hero-badge">PE6201 · EMERGING AI TECHNOLOGIES</div>
      <h1>Resume-JD Matching and Human Review Assistant</h1>
      <p>Compare job-relevant evidence with a transparent baseline and one
      structured foundation-model call, while keeping uncertain cases under
      human review.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

metric_one, metric_two, metric_three = st.columns(3)
metric_one.metric("LLM strict accuracy", "75%", help="30 correct cases out of 40")
metric_two.metric("Qualified-candidate recall", "85%", help="17 direct matches out of 20")
metric_three.metric("Manual-review rate", "25%", help="10 ambiguous cases routed to a person")

st.markdown('<div class="section-kicker">Step 1 · Input</div>', unsafe_allow_html=True)
st.markdown("## Compare one role with one resume")
input_left, input_right = st.columns(2, gap="large")
with input_left:
    job_description = st.text_area(
        "Job description",
        DEFAULT_JD,
        height=245,
        help="Paste the role requirements and responsibilities.",
    )
with input_right:
    resume = st.text_area(
        "Resume",
        DEFAULT_RESUME,
        height=245,
        help="Use synthetic data for the course demonstration.",
    )

with st.expander("Privacy check · preview the resume after local redaction", expanded=False):
    st.caption("Names, email addresses, and phone numbers are removed before the API call.")
    st.code(redact_pii(resume), language=None)

st.markdown('<div class="section-kicker">Step 2 · Compare</div>', unsafe_allow_html=True)
st.markdown("## Review the baseline and AI outputs")
baseline_tab, ai_tab = st.tabs(["Keyword baseline", "AI semantic comparison"])

with baseline_tab:
    st.caption("Transparent and reproducible, but unable to interpret context or negation.")
    if st.button("Run keyword baseline", type="primary", use_container_width=True):
        try:
            result = keyword_match(job_description, resume)
            with st.container(border=True):
                score_col, label_col = st.columns([1, 2])
                score_col.metric("Keyword score", f"{result.score}%")
                label_col.markdown("**Decision-support label**")
                label_col.markdown(
                    f'<span class="result-label">{result.verdict}</span>',
                    unsafe_allow_html=True,
                )
                st.divider()
                matched_col, missing_col = st.columns(2)
                matched_col.markdown("**Matched skills**")
                matched_col.write(", ".join(result.matched_skills) or "None")
                missing_col.markdown("**Missing skills**")
                missing_col.write(", ".join(result.missing_skills) or "None")
        except ValueError as exc:
            st.error(str(exc))

with ai_tab:
    st.caption("One structured model call that returns evidence, gaps, and an abstention when uncertain.")
    if not (os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")):
        st.info(
            "AI comparison is disabled until OPENROUTER_API_KEY is added to a "
            "local .env file. The key must never be committed to the repository."
        )

    if st.button("Run AI comparison", type="primary", use_container_width=True):
        try:
            with st.spinner("Comparing job-relevant evidence..."):
                result = match_with_openai(job_description, resume)
            with st.container(border=True):
                score_col, label_col = st.columns([1, 2])
                score_col.metric("AI score", f"{result.score}%")
                label_col.markdown("**Decision-support label**")
                label_col.markdown(
                    f'<span class="result-label">{result.verdict}</span>',
                    unsafe_allow_html=True,
                )
                st.divider()
                strengths_col, gaps_col = st.columns(2, gap="large")
                with strengths_col:
                    st.markdown("**Strengths**")
                    for item in result.strengths:
                        st.markdown(f"- {item}")
                with gaps_col:
                    st.markdown("**Gaps**")
                    for item in result.gaps:
                        st.markdown(f"- {item}")
                st.markdown("**Resume evidence used**")
                for item in result.evidence:
                    st.markdown(f"- {item}")
        except Exception as exc:
            st.error(f"AI comparison could not run: {exc}")

st.warning(
    "Human confirmation is required. This course prototype must not make an "
    "employment decision or automatically reject a candidate."
)
st.markdown(
    '<div class="footer-note">Han Haochen · PE6201 · Section C · Synthetic demonstration data only</div>',
    unsafe_allow_html=True,
)
