from evaluate import calculate_metrics


def test_calculate_metrics_handles_abstention():
    metrics = calculate_metrics(
        ["MATCH", "MATCH", "NO_MATCH", "NO_MATCH"],
        ["MATCH", "MANUAL_REVIEW", "NO_MATCH", "MATCH"],
    )

    assert metrics["coverage"] == 0.75
    assert metrics["strict_accuracy"] == 0.5
    assert metrics["manual_review_rate"] == 0.25
    assert metrics["selective_accuracy"] == 0.667
    assert metrics["qualified_recall"] == 0.5
    assert metrics["safe_review_recall"] == 1.0
