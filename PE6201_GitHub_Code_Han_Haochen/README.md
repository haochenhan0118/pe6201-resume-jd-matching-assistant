# Resume-JD Matching Assistant

Minimal PE6201 course prototype comparing a transparent keyword baseline with
one structured model call routed through OpenRouter.

## Intended use

The app supports a human reviewer by comparing job-relevant evidence in one job
description and one resume. It must not automatically reject or hire a person.

## What it includes

- Streamlit user interface
- keyword-overlap baseline
- local redaction of common names, email addresses and phone numbers
- one OpenRouter API call with a validated structured output
- manual-review outcome for ambiguous cases
- automated tests for the baseline and redaction logic
- deterministic synthetic development and test cases
- reproducible evaluation metrics and CSV outputs

## Setup

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The keyword baseline works without an API key.

For the AI comparison, copy `.env.example` to `.env`, then replace the example
value with an OpenRouter API key. Never commit `.env`. Existing local files that
use `OPENAI_API_KEY` are accepted as a compatibility alias when the key starts
with `sk-or-`.

```bash
cp .env.example .env
streamlit run app.py
```

## Run tests

```bash
pytest -q
```

## Generate data and evaluate

The synthetic data generator fixes each label before either system is evaluated:

```bash
python generate_dataset.py
python evaluate.py
```

After the API key and provider are confirmed, run the AI comparison as well:

```bash
python evaluate.py --include-ai
```

The outputs are written to `results/predictions.csv` and `results/summary.json`.

The current held-out run is summarized in `results/evaluation_report.md`. On 40
synthetic test cases, the LLM matcher achieved 75% strict accuracy versus 25% for
the keyword baseline and 50% for the majority-class baseline. These figures are
course evidence only and do not establish real-world hiring validity.

## Current limits

- The baseline recognizes only the fixed skill vocabulary in `baseline.py`.
- Redaction covers common direct identifiers but is not production-grade.
- The prototype accepts pasted text only.
- Results are decision support, not hiring decisions.
- The synthetic dataset covers only one junior data-analyst role and cannot establish
  production hiring validity.
