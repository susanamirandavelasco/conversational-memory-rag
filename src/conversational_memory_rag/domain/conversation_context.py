from dataclasses import dataclass, field

from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role

class ConversationContext:

    def __init__(
        self,
        messages: tuple[Message, ...],
        rewritten_question: str | None = None
    ):
        self._messages = messages
        self._rewritten_question = rewritten_question

    @property
    def messages(self) -> tuple[Message, ...]:
        return self._messages


    def get_last_user_message(self) -> Message:

        for message in reversed(self._messages):

            if message.role == Role.USER:
                return message

        raise ValueError("Conversation has no user messages.")

    @property
    def rewritten_question(self) -> str | None:
        return self._rewritten_question