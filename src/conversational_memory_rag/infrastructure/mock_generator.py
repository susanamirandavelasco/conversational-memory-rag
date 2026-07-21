from conversational_memory_rag.application.generator import Generator


class MockGenerator(Generator):

    def generate(self, prompt: str) -> str:
        return "This is a mock response."