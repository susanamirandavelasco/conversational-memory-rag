from conversational_memory_rag.application.question_rewriter import (
    QuestionRewriter
)

from conversational_memory_rag.domain.conversation_context import (
    ConversationContext
)


class NoOpQuestionRewriter(QuestionRewriter):

    def rewrite(
        self,
        conversation_context: ConversationContext
    ) -> ConversationContext:

        question = (
            conversation_context
            .get_last_user_message()
            .content
        )

        return ConversationContext(
            messages=conversation_context.messages,
            rewritten_question=question,
            summary=conversation_context.summary
        )