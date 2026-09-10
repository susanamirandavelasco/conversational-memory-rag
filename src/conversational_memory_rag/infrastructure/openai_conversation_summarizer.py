from openai import OpenAI

from conversational_memory_rag.application.conversation_summarizer import (
    ConversationSummarizer,
)
from conversational_memory_rag.application.conversation_summarizer_prompt_builder import (
    ConversationSummarizerPromptBuilder,
)
from conversational_memory_rag.config import Settings
from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.summary import Summary


class OpenAIConversationSummarizer(ConversationSummarizer):
    def __init__(
        self,
        prompt_builder: ConversationSummarizerPromptBuilder,
        client: OpenAI | None = None,
        model: str | None = None,
    ):
        settings = Settings.from_env()
        self._client = client or OpenAI(
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self._model = model or settings.summarizer_model
        self._prompt_builder = prompt_builder

    def summarize(self, conversation_context: ConversationContext) -> Summary:

        prompt = self._prompt_builder.build(conversation_context)

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt.content}],
            temperature=0,
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI returned an empty summary.")
        summary = content.strip()

        return Summary(content=summary)
