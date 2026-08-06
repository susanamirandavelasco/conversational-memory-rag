from conversational_memory_rag.application.question_rewriter_prompt_builder import QuestionRewriterPromptBuilder

from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.prompt import Prompt


class DefaultQuestionRewriterPromptBuilder(
    QuestionRewriterPromptBuilder
):

    def build(
        self,
        conversation_context: ConversationContext
    ) -> Prompt:

        history = []

        for message in conversation_context.messages:

            history.append(
                f"{message.role.name}: {message.content}"
            )

        conversation = "\n".join(history)

        return Prompt(
            content=f"""
                Rewrite the user's last question so it is completely standalone.

                Keep the meaning exactly the same.

                Do not answer the question.

                Only return the rewritten question.

                Conversation:

                {conversation}
                """
                        )