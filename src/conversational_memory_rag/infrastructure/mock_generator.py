from conversational_memory_rag.application.generator import Generator


class MockGenerator(Generator):

    def generate(self, prompt: str) -> str:
        return f"""
            From Mock Generator
            {prompt}
            """