from scam_engine import analyze, QUIZ

def test_quiz_matches_engine():
    for text, is_scam, _ in QUIZ:
        level, _f = analyze(text)
        assert (level != "safe-looking") == is_scam, text

def test_empty():
    assert analyze("")[0] == "safe-looking"
