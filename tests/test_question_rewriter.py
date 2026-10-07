from conversational_memory_rag.domain.conversation_context import ConversationContext
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role
from conversational_memory_rag.domain.summary import Summary
from conversational_memory_rag.infrastructure.no_op_question_rewriter import (
    NoOpQuestionRewriter,
)


def test_no_op_rewriter_uses_last_user_message_and_preserves_context():
    messages = (
        Message(role=Role.USER, content="Tell me about Bedrock"),
        Message(role=Role.ASSISTANT, content="Bedrock is..."),
        Message(role=Role.USER, content="How much does it cost?"),
    )
    summary = Summary("The user is asking about Amazon Bedrock.")

    result = NoOpQuestionRewriter().rewrite(
        ConversationContext(messages=messages, summary=summary)
    )

    assert result.rewritten_question == "How much does it cost?"
    assert result.messages == messages
    assert result.summary is summary
