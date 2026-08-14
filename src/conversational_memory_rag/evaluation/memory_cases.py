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

def build_mem_001() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "My favorite AWS service is Amazon Bedrock."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Got it. Your favorite AWS service is Amazon Bedrock."
    )

    add_message(
        conversation,
        Role.USER,
        "I am building a chatbot."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "That sounds interesting."
    )

    add_message(
        conversation,
        Role.USER,
        "The chatbot will use generative AI."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Generative AI can be useful for that."
    )

    add_message(
        conversation,
        Role.USER,
        "What is my favorite AWS service?"
    )

    return EvaluationCase(
        case_id="MEM-001",
        name="Long-term fact memory",
        category="long_term_memory",
        conversation=conversation,
        expected_answer="Amazon Bedrock"
    )

def build_mem_002() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "I'm building a chatbot."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "What platform are you considering?"
    )

    add_message(
        conversation,
        Role.USER,
        "Amazon Bedrock."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Bedrock can be used for generative AI applications."
    )

    add_message(
        conversation,
        Role.USER,
        "Which platform did I say I'm considering?"
    )

    return EvaluationCase(
        case_id="MEM-002",
        name="Recent memory",
        category="recent_memory",
        conversation=conversation,
        expected_answer="Amazon Bedrock"
    )

def build_mem_003() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "I'm building a customer-support chatbot for an online store."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Got it."
    )

    add_message(
        conversation,
        Role.USER,
        "I want to use generative AI."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "That can be useful for conversational applications."
    )

    add_message(
        conversation,
        Role.USER,
        "The application will run in AWS."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "AWS provides several services for generative AI."
    )

    add_message(
        conversation,
        Role.USER,
        "What am I building?"
    )

    return EvaluationCase(
        case_id="MEM-003",
        name="Semantic conversational memory",
        category="semantic_memory",
        conversation=conversation,
        expected_answer="A customer-support chatbot for an online store"
    )

def build_mem_004() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "The chatbot must support Spanish and English."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Understood."
    )

    add_message(
        conversation,
        Role.USER,
        "I like coffee."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Nice."
    )

    add_message(
        conversation,
        Role.USER,
        "I also like dogs."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Dogs are great."
    )

    add_message(
        conversation,
        Role.USER,
        "Which languages must my chatbot support?"
    )

    return EvaluationCase(
        case_id="MEM-004",
        name="Memory with irrelevant noise",
        category="noise_resilience",
        conversation=conversation,
        expected_answer="Spanish and English"
    )

def build_mem_005() -> EvaluationCase:

    conversation = Conversation()

    add_message(
        conversation,
        Role.USER,
        "I'm building an application with Amazon Bedrock."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Got it."
    )

    add_message(
        conversation,
        Role.USER,
        "The application will use generative AI."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Understood."
    )

    add_message(
        conversation,
        Role.USER,
        "It will run in AWS."
    )

    add_message(
        conversation,
        Role.ASSISTANT,
        "Sounds good."
    )

    add_message(
        conversation,
        Role.USER,
        "Which database did I say I was going to use?"
    )

    return EvaluationCase(
        case_id="MEM-005",
        name="Unknown information should not be invented",
        category="negative_memory",
        conversation=conversation,
        expected_answer="No database was specified"
    )

def get_memory_evaluation_cases() -> list[EvaluationCase]:

    return [
        build_mem_001(),
        build_mem_002(),
        build_mem_003(),
        build_mem_004(),
        build_mem_005(),
    ]