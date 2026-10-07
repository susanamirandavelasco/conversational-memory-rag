from openai import OpenAI

from conversational_memory_rag.application.generator import Generator
from conversational_memory_rag.config import Settings
from conversational_memory_rag.domain.prompt import Prompt


class OpenAIGenerator(Generator):
    def __init__(self, client: OpenAI | None = None, model: str | None = None):
        settings = Settings.from_env()
        self._client = client or OpenAI(
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self._model = model or settings.generation_model

    def generate(self, prompt: Prompt) -> str:

        response = self._client.chat.completions.create(
            model=self._model, messages=[{"role": "user", "content": prompt.content}]
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI returned an empty response.")
        return content
