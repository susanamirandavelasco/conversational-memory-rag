from dataclasses import dataclass, field

from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role

class ConversationContext:

    def __init__(
        self,
        messages: tuple[Message, ...]
    ):
        self._messages = messages

    @property
    def messages(self) -> tuple[Message, ...]:
        return self._messages


    def get_last_user_message(self) -> Message:

        for message in reversed(self._messages):

            if message.role == Role.USER:
                return message

        raise ValueError("Conversation has no user messages.")