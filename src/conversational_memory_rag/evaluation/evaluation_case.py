from dataclasses import dataclass

from conversational_memory_rag.domain.conversation import Conversation


@dataclass
class EvaluationCase:
    case_id: str
    name: str
    category: str
    conversation: Conversation
    expected_answer: str