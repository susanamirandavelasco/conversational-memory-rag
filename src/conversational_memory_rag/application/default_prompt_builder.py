from conversational_memory_rag.application.prompt_builder import PromptBuilder

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.retrieval_result import RetrievalResult



class DefaultPromptBuilder(PromptBuilder):

    def build(
        self,
        conversation: Conversation,
        retrieval_result: RetrievalResult
    ) -> str:

        question = conversation.get_last_message().content

        context = "\n\n".join(
            chunk.content
            for chunk in retrieval_result.chunks
        )

        return f"""
            You are an AWS Bedrock expert.
            Answer only using the following context. 

            Context:
            {context}

            Question:
            {question}

            Answer:
            """