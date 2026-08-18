from conversational_memory_rag.evaluation.engine_factory import (
    build_engine
)

from conversational_memory_rag.evaluation.evaluation_runner import (
    EvaluationRunner
)

from conversational_memory_rag.evaluation.llm_judge_evaluator import (
    LLMJudgeEvaluator
)

from conversational_memory_rag.evaluation.question_rewriter_cases import (
    get_question_rewriter_cases
)


def main():

    configurations = [
        ("ON", True),
        #("ON", True),
    ]

    cases = get_question_rewriter_cases()

    for label, enabled in configurations:

        print("\n" + "=" * 80)
        print(f"QUESTION REWRITER = {label}")
        print("=" * 80)

        engine = build_engine(
            n_results=3,
            use_question_rewriter=enabled
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