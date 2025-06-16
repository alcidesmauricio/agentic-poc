from backend.interfaces.openai_client import OpenAIClient

class DecisionLayer:
    def __init__(self):
        self.llm = OpenAIClient()

    def decide(self, user_input: str) -> str:
        return self.llm.complete_with_tools(user_input)
