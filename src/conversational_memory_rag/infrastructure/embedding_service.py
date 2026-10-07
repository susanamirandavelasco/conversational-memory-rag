from openai import OpenAI

from conversational_memory_rag.config import Settings


class EmbeddingService:
    def __init__(self, client: OpenAI | None = None, model: str | None = None):
        settings = Settings.from_env()
        self._client = client or OpenAI(
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self._model = model or settings.embedding_model

    def generate(self, text: str) -> list[float]:

        response = self._client.embeddings.create(model=self._model, input=text)

        return response.data[0].embedding
