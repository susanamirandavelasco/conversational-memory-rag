from openai import OpenAI

from conversational_memory_rag.application.question_rewriter import QuestionRewriter
from conversational_memory_rag.application.question_rewriter_prompt_builder import (
    QuestionRewriterPromptBuilder,
)
from conversational_memory_rag.config import Settings
from conversational_memory_rag.domain.conversation_context import ConversationContext


class OpenAIQuestionRewriter(QuestionRewriter):
    def __init__(
        self,
        prompt_builder: QuestionRewriterPromptBuilder,
        client: OpenAI | None = None,
        model: str | None = None,
    ):

        settings = Settings.from_env()
        self._client = client or OpenAI(
            timeout=settings.openai_timeout_seconds,
            max_retries=settings.openai_max_retries,
        )
        self._model = model or settings.question_rewriter_model
        self._prompt_builder = prompt_builder

    def rewrite(self, conversation_context: ConversationContext) -> ConversationContext:

        prompt = self._prompt_builder.build(conversation_context)

        response = self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt.content}],
            temperature=0,
        )

        content = response.choices[0].message.content
        if content is None:
            raise ValueError("OpenAI returned an empty rewritten question.")

        rewritten_question = content.strip()

        return ConversationContext(
            messages=conversation_context.messages,
            rewritten_question=rewritten_question,
            summary=conversation_context.summary,
        )
