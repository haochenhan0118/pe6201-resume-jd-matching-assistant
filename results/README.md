# Evaluation Explainer

## Evaluation question

The evaluation asks whether a structured foundation-model comparison provides
more useful classification than literal keyword overlap on the same 40 held-out
synthetic cases. It also measures the operational cost of sending uncertain
cases to a person.

## Systems compared

1. **Majority baseline:** predicts the most common test label for every case.
2. **Keyword baseline:** measures overlap using the fixed vocabulary in
   `baseline.py`.
3. **LLM matcher:** uses the prompt in `prompt.txt` and the validated schema in
   `matcher.py`.

## Metrics

| Metric | Definition |
|---|---|
| Strict accuracy | Correct predictions divided by all test cases; `MANUAL_REVIEW` counts as incorrect |
| Qualified recall | True `MATCH` cases directly predicted as `MATCH` divided by all true `MATCH` cases |
| Manual-review rate | Share of cases returned as `MANUAL_REVIEW` |
| Selective accuracy | Accuracy only among cases receiving a definite prediction |
| Safe-review recall | Qualified cases predicted `MATCH` or routed to manual review |

Strict accuracy prevents abstention from being counted as success. Selective
accuracy shows answer quality at the achieved coverage, while manual-review rate
shows the human workload required to obtain that quality.

## Run the evaluation

The baselines require no API key:

```bash
python evaluate.py
```

To include the LLM matcher, create a local `.env` from `.env.example`, add an
OpenRouter key, and run:

```bash
python evaluate.py --include-ai
```

## Checked-in outputs

- `summary.json` contains the aggregate metrics.
- `predictions.csv` contains one row per system and test case.
- `evaluation_report.md` explains the findings and limitations.

The checked-in LLM run reached 75% strict accuracy, 85% qualified recall, 25%
manual review, and 100% selective accuracy on 30 definite answers. These values
describe this synthetic test only. They do not establish real-world accuracy,
fairness, or suitability for automated employment decisions.
