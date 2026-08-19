from conversational_memory_rag.evaluation.engine_factory import (
    build_engine
)

from conversational_memory_rag.evaluation.evaluation_runner import (
    EvaluationRunner
)

from conversational_memory_rag.evaluation.llm_judge_evaluator import (
    LLMJudgeEvaluator
)

from conversational_memory_rag.evaluation.memory_cases import (
    get_memory_evaluation_cases
)


def main():

    configurations = [
        ("OFF", False),
        ("ON", True),
    ]

    all_cases = get_memory_evaluation_cases()

    cases = [
        case
        for case in all_cases
        if case.case_id in ("MEM-001", "MEM-004")
    ]

    for label, enabled in configurations:

        print("\n" + "=" * 80)
        print(f"SUMMARY = {label}")
        print("=" * 80)

        engine = build_engine(
            n_results=3,
            use_question_rewriter=True,
            use_summary=enabled
        )

        runner = EvaluationRunner(
            engine=engine,
            evaluator=LLMJudgeEvaluator()
        )

        results = runner.run(cases)

        for result in results:

            score = result.evaluation_score

            print(
                f"\n{result.case_id}"
                f" | Passed: {score.passed}"
                f" | Score: {score.score}"
            )

            print(f"Actual: {result.actual_answer}")
            print(f"Reason: {score.reason}")


if __name__ == "__main__":
    main()