from conversational_memory_rag.application.conversation_engine import (
    ConversationEngine
)

from conversational_memory_rag.evaluation.evaluation_case import (
    EvaluationCase
)

from conversational_memory_rag.evaluation.evaluation_result import (
    EvaluationResult
)


class EvaluationRunner:

    def __init__(
        self,
        engine: ConversationEngine
    ):
        self._engine = engine

    def run_case(
        self,
        case: EvaluationCase
    ) -> EvaluationResult:

        actual_answer = self._engine.ask(
            case.conversation
        )

        return EvaluationResult(
            case_id=case.case_id,
            case_name=case.name,
            category=case.category,
            expected_answer=case.expected_answer,
            actual_answer=actual_answer
        )

    def run(
        self,
        cases: list[EvaluationCase]
    ) -> list[EvaluationResult]:

        results = []

        for case in cases:

            result = self.run_case(case)

            results.append(result)

        return results