from dataclasses import dataclass, field

class Prompt:

    def __init__(
        self,
        content: str
    ):
        self._content = content

    @property
    def content(self) -> str:
        return self._content