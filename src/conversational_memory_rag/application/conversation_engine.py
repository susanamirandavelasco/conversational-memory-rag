from conversational_memory_rag.application.generator import Generator
from conversational_memory_rag.application.prompt_builder import PromptBuilder
from conversational_memory_rag.application.default_prompt_builder import DefaultPromptBuilder
from conversational_memory_rag.application.retriever import Retriever
from conversational_memory_rag.application.memory_manager import MemoryManager

from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role
from conversational_memory_rag.domain.conversation import Conversation


class ConversationEngine:

    def __init__(
        self,
        memory_manager: MemoryManager,
        prompt_builder: PromptBuilder,
        generator: Generator,
        retriever: Retriever
    ):
        self._memory_manager = memory_manager
        self._prompt_builder = prompt_builder
        self._generator = generator
        self._retriever = retriever

    def ask(
        self,
        conversation: Conversation
    ) -> str:

        # 1. Get the question
        user_question = conversation.get_last_message().content

        # 2. Get the memory
        conversation_context = self._memory_manager.get_context(conversation)

        # 3. Get the context (knowledge)
        retrieval_result = self._retriever.retrieve(query=user_question)

        # 4. Build the prompt
        prompt = self._prompt_builder.build(
            conversation_context=conversation_context,
            retrieval_result=retrieval_result)

        # 5. Build the response
        response = self._generator.generate(prompt)

        # 6. Add the response to the conversation 
        conversation.add_message(
            Message(
                role=Role.ASSISTANT,
                content=response
            )
        )

        return response