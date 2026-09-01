from openai import OpenAI

from conversational_memory_rag.application.question_rewriter import QuestionRewriter
from conversational_memory_rag.application.question_rewriter_prompt_builder import QuestionRewriterPromptBuilder

from conversational_memory_rag.domain.conversation_context import ConversationContext


class OpenAIQuestionRewriter(QuestionRewriter):

    def __init__(
        self,
        prompt_builder: QuestionRewriterPromptBuilder
    ):

        self._client = OpenAI()
        self._prompt_builder = prompt_builder

    def rewrite(
        self,
        conversation_context: ConversationContext
    ) -> ConversationContext:

        prompt = self._prompt_builder.build(
            conversation_context
        )

        response = self._client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt.content
                }
            ],
            temperature=0
        )

        rewritten_question = (
            response
            .choices[0]
            .message
            .content
            .strip()
        )

        return ConversationContext(
            messages=conversation_context.messages,
            rewritten_question=rewritten_question,
            summary=conversation_context.summary
        )