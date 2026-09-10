from conversational_memory_rag.config import Settings


def test_settings_can_be_overridden_from_environment(monkeypatch):
    monkeypatch.setenv("GENERATION_MODEL", "test-model")
    monkeypatch.setenv("CHROMA_PATH", "/tmp/test-chroma")
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", "12.5")
    monkeypatch.setenv("OPENAI_MAX_RETRIES", "4")

    settings = Settings.from_env()

    assert settings.generation_model == "test-model"
    assert settings.chroma_path == "/tmp/test-chroma"
    assert settings.openai_timeout_seconds == 12.5
    assert settings.openai_max_retries == 4
