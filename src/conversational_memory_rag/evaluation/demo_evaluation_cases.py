from conversational_memory_rag.evaluation.memory_cases import (
    get_memory_evaluation_cases
)


def main():

    cases = get_memory_evaluation_cases()

    for case in cases:

        print("\n" + "=" * 80)

        print(f"{case.case_id} - {case.name}")
        print(f"Category: {case.category}")
        print(f"Expected: {case.expected_answer}")

        print("\nConversation:")

        for message in case.conversation.messages:
            print(
                f"{message.role.name}: {message.content}"
            )


if __name__ == "__main__":
    main()