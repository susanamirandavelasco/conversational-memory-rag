from conversational_memory_rag.application.prompt_builder import PromptBuilder

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.retrieval_result import RetrievalResult
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.prompt import Prompt


SYSTEM_PROMPT = """
    You are an AWS Bedrock expert.

    Answer only using the provided context.
    """

class DefaultPromptBuilder(PromptBuilder):

    def build(
        self,
        conversation_context: tuple[Message, ...],
        retrieval_result: RetrievalResult
    ) -> str:

        history = "\n".join(
            f"{message.role.name}: {message.content}"
            for message in conversation_context.messages
        )

        retrieved_context = "\n\n".join(
            chunk.content
            for chunk in retrieval_result.chunks
        )

        return Prompt(
                content=f"""
                    {SYSTEM_PROMPT}
                    Conversation:
                    {history}
                    Retrieved Context:
                    {retrieved_context}
                    Assistant:
                    """
                    )