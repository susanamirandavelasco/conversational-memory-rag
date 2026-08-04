from conversational_memory_rag.application.question_rewriter import QuestionRewriter

from conversational_memory_rag.domain.conversation_context import ConversationContext


class MockQuestionRewriter(QuestionRewriter):

    def rewrite(
        self,
        conversation_context: ConversationContext
    ) -> ConversationContext:

        last_question = conversation_context.get_last_user_message()

        return ConversationContext(
            messages=conversation_context.messages,
            rewritten_question=last_question.content
        )