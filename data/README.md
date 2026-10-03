# Dataset Explainer

## Purpose

`cases.csv` is a deterministic synthetic dataset used to compare the keyword
baseline and LLM matcher. It contains no real applicant information and is not
evidence of production hiring performance.

## Scope and splits

- 60 resume and job-description pairs for one Junior Data Analyst role
- 20 development cases for prompt and threshold iteration
- 40 held-out test cases used for the reported results
- 20 `MATCH` and 20 `NO_MATCH` labels in the test split
- standard, hard, easy, and adversarial cases

The scenarios cover direct skill evidence, semantic paraphrases, missing
evidence, negated skills, copied keywords, and one prompt-injection attempt.
Ground-truth labels are assigned by scenario rules before either matcher runs.

## Columns

| Column | Meaning |
|---|---|
| `case_id` | Stable case identifier |
| `split` | `development` or `test` |
| `job_description` | Synthetic role text |
| `resume` | Synthetic candidate text |
| `ground_truth` | Fixed `MATCH` or `NO_MATCH` label |
| `difficulty` | Scenario difficulty category |
| `label_basis` | Short reason for the assigned label |

## Reproduce the data

From the repository root, run:

```bash
python generate_dataset.py
```

The generator uses fixed templates and ordering, so rerunning it produces the
same labelled cases. Regenerating the file will overwrite `data/cases.csv`.

## Limitations

The project author designed the scenarios and labels. The templates repeat,
the test distribution is artificially balanced, and only one job family is
represented. An externally labelled dataset with independent recruiter review
is required before making claims about real applicants, fairness, or deployment
performance.
