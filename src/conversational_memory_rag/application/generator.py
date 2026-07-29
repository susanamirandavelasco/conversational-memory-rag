from abc import ABC, abstractmethod

from conversational_memory_rag.domain.prompt import Prompt



class Generator(ABC):

    @abstractmethod
    def generate(self, prompt: Prompt) -> str:
        pass