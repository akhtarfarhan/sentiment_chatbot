from app.chat import respond

def test_basic_reply():
    ans, sent = respond("pytest", "Hi!")
    assert ans and isinstance(ans, str)
    assert sent in {"POSITIVE", "NEGATIVE", "NEUTRAL"}
