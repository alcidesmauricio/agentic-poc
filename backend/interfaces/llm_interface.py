from abc import ABC, abstractmethod

class LLMInterface(ABC):
    @abstractmethod
    def complete(self, prompt: str) -> str:
        pass

    @abstractmethod
    def complete_with_tools(self, user_input: str) -> str:
        """Processa uma entrada com suporte a ferramentas"""
        pass
