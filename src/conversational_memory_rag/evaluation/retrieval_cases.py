from conversational_memory_rag.domain.conversation import Conversation
from conversational_memory_rag.domain.message import Message
from conversational_memory_rag.domain.role import Role

from conversational_memory_rag.evaluation.evaluation_case import EvaluationCase


def build_case(
    case_id: str,
    question: str,
    expected_answer: str
) -> EvaluationCase:

    conversation = Conversation()

    conversation.add_message(
        Message(
            role=Role.USER,
            content=question
        )
    )

    return EvaluationCase(
        case_id=case_id,
        name=question,
        category="retrieval",
        conversation=conversation,
        expected_answer=expected_answer
    )

def get_retrieval_evaluation_cases():

    return [
        build_case(
            case_id="RET-001",
            question="What is Bedrock Data Automation?",
            expected_answer="Bedrock Data Automation (BDA) is a cloud-based service that simplifies the process of extracting valuable insights from unstructured content—such as documents, images, video, and audio. "
        ),
        build_case(
            case_id="RET-002",
            question="How Bedrock Data Automation works?",
            expected_answer="Bedrock Data Automation (BDA) lets you configure output based on your processing needs for a specific data type: documents, images, video or audio."
        ),
        build_case(
            case_id="RET-003",
            question="What is RAG",
            expected_answer="RAG is a technique that uses information from data sources to improve the relevancy and accuracy of generated responses."
        ),
    ]