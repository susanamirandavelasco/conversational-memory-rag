from conversational_memory_rag.application.conversation_engine import (
    ConversationEngine
)

from conversational_memory_rag.evaluation.evaluation_runner import (
    EvaluationRunner
)

from conversational_memory_rag.evaluation.memory_cases import (
    get_memory_evaluation_cases
)

from conversational_memory_rag.evaluation.llm_judge_evaluator import (
    LLMJudgeEvaluator
)

from conversational_memory_rag.evaluation.engine_factory import build_engine


def main():

    engine = build_engine()

    runner = EvaluationRunner(
        engine=engine,
        evaluator=LLMJudgeEvaluator()
        )

    cases = get_memory_evaluation_cases()

    results = runner.run(cases)

    for result in results:

        print("\n" + "=" * 80)

        print(
            f"{result.case_id} - {result.case_name}"
        )

        print(
            f"Category: {result.category}"
        )

        print(
            f"\nExpected:\n{result.expected_answer}"
        )

        print(
            f"\nActual:\n{result.actual_answer}"
        )

        score = result.evaluation_score

        print(
            f"\nPassed: {score.passed}"
        )

        print(
            f"Score: {score.score}"
        )

        print(
            f"Reason: {score.reason}"
        )

    passed = sum(
        1
        for result in results
        if result.evaluation_score
        and result.evaluation_score.passed
    )

    total = len(results)

    average_score = sum(
        result.evaluation_score.score
        for result in results
        if result.evaluation_score
    ) / total

    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY")
    print(f"Passed: {passed}/{total}")
    print(f"Average score: {average_score:.2f}")
 


if __name__ == "__main__":
    main()