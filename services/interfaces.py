

class ICache:

    def get(self, key: str) -> str:
        pass

    def set(self, key: str, value: str) -> None:
        pass

from abc import ABC, abstractmethod
class LLMModel(ABC):
    @abstractmethod
    def prompt(self, prompt: str) -> str:
        pass
    @abstractmethod
    def setup(self)->None:
        pass