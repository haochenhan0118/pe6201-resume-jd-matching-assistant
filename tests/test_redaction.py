from matcher import redact_pii


def test_redacts_name_email_and_phone():
    resume = "Alex Tan\nalex.tan@example.com | +65 9123 4567\nPython and SQL"
    result = redact_pii(resume)

    assert "Alex Tan" not in result
    assert "alex.tan@example.com" not in result
    assert "9123 4567" not in result
    assert "Python and SQL" in result

