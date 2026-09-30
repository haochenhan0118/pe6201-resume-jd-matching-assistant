"""Evaluate the keyword baseline and, optionally, the OpenAI matcher."""

from __future__ import annotations

import argparse
from collections import Counter
import csv
import json
from pathlib import Path
from typing import Callable

from baseline import keyword_match
from matcher import match_with_openai


PROJECT_DIR = Path(__file__).resolve().parent


def calculate_metrics(labels: list[str], predictions: list[str]) -> dict[str, float | int]:
    if not labels or len(labels) != len(predictions):
        raise ValueError("Labels and predictions must be non-empty and the same length.")

    total = len(labels)
    answered = [index for index, value in enumerate(predictions) if value != "MANUAL_REVIEW"]
    strict_correct = sum(label == prediction for label, prediction in zip(labels, predictions))
    correct_answered = sum(labels[index] == predictions[index] for index in answered)
    positives = sum(label == "MATCH" for label in labels)
    true_positive = sum(
        label == "MATCH" and prediction == "MATCH"
        for label, prediction in zip(labels, predictions)
    )
    safe_positive = sum(
        label == "MATCH" and prediction != "NO_MATCH"
        for label, prediction in zip(labels, predictions)
    )

    return {
        "cases": total,
        "strict_accuracy": round(strict_correct / total, 3),
        "coverage": round(len(answered) / total, 3),
        "manual_review_rate": round(1 - len(answered) / total, 3),
        "selective_accuracy": round(correct_answered / len(answered), 3) if answered else 0.0,
        "qualified_recall": round(true_positive / positives, 3) if positives else 0.0,
        "safe_review_recall": round(safe_positive / positives, 3) if positives else 0.0,
    }


def _load_test_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as file:
        return [row for row in csv.DictReader(file) if row["split"] == "test"]


def _predict_baseline(row: dict[str, str]) -> tuple[str, int]:
    result = keyword_match(row["job_description"], row["resume"])
    return result.verdict, result.score


def _predict_ai(row: dict[str, str]) -> tuple[str, int]:
    result = match_with_openai(row["job_description"], row["resume"])
    return result.verdict, result.score


def _run_system(
    name: str,
    rows: list[dict[str, str]],
    predictor: Callable[[dict[str, str]], tuple[str, int]],
) -> tuple[list[dict[str, str | int]], dict[str, float | int]]:
    output_rows: list[dict[str, str | int]] = []
    for index, row in enumerate(rows, start=1):
        prediction, score = predictor(row)
        output_rows.append(
            {
                "case_id": row["case_id"],
                "difficulty": row["difficulty"],
                "ground_truth": row["ground_truth"],
                "system": name,
                "prediction": prediction,
                "score": score,
            }
        )
        print(f"{name}: {index}/{len(rows)}", end="\r")
    print()
    metrics = calculate_metrics(
        [row["ground_truth"] for row in rows],
        [str(row["prediction"]) for row in output_rows],
    )
    return output_rows, metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-ai", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    rows = _load_test_rows(PROJECT_DIR / "data" / "cases.csv")
    if args.limit:
        rows = rows[: args.limit]

    all_predictions: list[dict[str, str | int]] = []
    summary: dict[str, dict[str, float | int]] = {}

    baseline_rows, baseline_metrics = _run_system("keyword_baseline", rows, _predict_baseline)
    all_predictions.extend(baseline_rows)
    summary["keyword_baseline"] = baseline_metrics

    majority_label = Counter(row["ground_truth"] for row in rows).most_common(1)[0][0]
    majority_predictions = [majority_label] * len(rows)
    summary["majority_baseline"] = calculate_metrics(
        [row["ground_truth"] for row in rows], majority_predictions
    )

    if args.include_ai:
        ai_rows, ai_metrics = _run_system("ai_matcher", rows, _predict_ai)
        all_predictions.extend(ai_rows)
        summary["ai_matcher"] = ai_metrics

    results_dir = PROJECT_DIR / "results"
    results_dir.mkdir(exist_ok=True)
    with (results_dir / "predictions.csv").open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(all_predictions[0]))
        writer.writeheader()
        writer.writerows(all_predictions)
    (results_dir / "summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
