from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role

from conversational_memory_rag.evaluation.evaluation_case import EvaluationCase


def add_message(
    conversation: Conversation,
    role: Role,
    content: str
) -> None:

    conversation.add_message(
        Message(
            role=role,
            content=content
        )
    )


def build_qr_001() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "Tell me about Amazon Bedrock."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Amazon Bedrock is an AWS service for building generative AI applications."
    )

    add_message(
        conversation,
        Role.USER,
        "How much does it cost?"
    )

    return EvaluationCase(
        case_id="QR-001",
        name="Resolve pronoun reference for pricing",
        category="question_rewriter",
        conversation=conversation,
        expected_answer=(
            "Amazon Bedrock pricing depends on the models "
            "and features used."
        )
    )


def build_qr_002() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "Tell me about Amazon Bedrock."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Amazon Bedrock provides access to foundation models."
    )

    add_message(
        conversation,
        Role.USER,
        "Does it support Claude?"
    )

    return EvaluationCase(
        case_id="QR-002",
        name="Resolve pronoun reference for model support",
        category="question_rewriter",
        conversation=conversation,
        expected_answer=(
            "Yes, Amazon Bedrock supports Anthropic Claude models."
        )
    )


def build_qr_003() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "What are Knowledge Bases for Amazon Bedrock?"
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "They provide managed capabilities for retrieval augmented generation."
    )

    add_message(
        conversation,
        Role.USER,
        "How do they work?"
    )

    return EvaluationCase(
        case_id="QR-003",
        name="Resolve plural reference for Knowledge Bases",
        category="question_rewriter",
        conversation=conversation,
        expected_answer=(
            "Amazon Bedrock Knowledge Bases retrieve relevant information "
            "from connected data sources to support retrieval augmented generation."
        )
    )


def get_question_rewriter_cases() -> list[EvaluationCase]:

    return [
        build_qr_001(),
        build_qr_002(),
        build_qr_003(),
    ]