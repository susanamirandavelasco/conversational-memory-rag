from unittest.mock import Mock

from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role
from conversational_memory_rag.domain.summary import Summary
from conversational_memory_rag.infrastructure.last_messages_memory_manager import (
    LastMessagesMemoryManager,
)


def _conversation_with_messages(count: int) -> Conversation:
    conversation = Conversation()
    for index in range(count):
        conversation.add_message(Message(role=Role.USER, content=f"message-{index}"))
    return conversation


def test_memory_returns_recent_window_without_summary_when_it_fits():
    summarizer = Mock()
    manager = LastMessagesMemoryManager(summarizer=summarizer, max_messages=3)
    conversation = _conversation_with_messages(3)

    context = manager.get_context(conversation)

    assert context.messages == conversation.messages
    assert context.summary is None
    summarizer.summarize.assert_not_called()


def test_memory_summarizes_full_conversation_and_keeps_recent_window():
    summarizer = Mock()
    summarizer.summarize.return_value = Summary("earlier facts")
    manager = LastMessagesMemoryManager(summarizer=summarizer, max_messages=2)
    conversation = _conversation_with_messages(4)

    context = manager.get_context(conversation)

    assert [message.content for message in context.messages] == [
        "message-2",
        "message-3",
    ]
    assert context.summary.content == "earlier facts"
    summary_context = summarizer.summarize.call_args.args[0]
    assert summary_context.messages == conversation.messages
