from typing import List, Dict
from backend.interfaces.llm_interface import LLMInterface
from backend.tools.registry import get_registered_tools
from .base import PlannerBase
from backend.interfaces.openai_client import OpenAIClient
import json

class LLMPlanner(PlannerBase):
    def __init__(self):
        self.llm = OpenAIClient()

    def generate_plan(self, user_input: str) -> List[Dict]:
        system_prompt = """
Você é um planejador de ações para um agente AI. Dado um input de um desenvolvedor, você deve escolher qual ferramenta (tool) usar.

Responda apenas com JSON conforme o exemplo:
[
    {
        "tool": "tool_name",
        "args": { "param": "value" }
    }
]
"""
        prompt = f"Usuário: {user_input}"
        tools = get_registered_tools()

        try:
            response = self.llm.client.chat.completions.create(
                model=self.llm.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                tools=tools,
                tool_choice="auto"
            )
            message = response.choices[0].message
            if hasattr(message, "tool_calls") and message.tool_calls:
                return [
                    {
                        "tool": call.function.name,
                        "args": json.loads(call.function.arguments)
                    }
                    for call in message.tool_calls
                ]
        except Exception as e:
            print(f"[Erro LLMPlanner]: {e}")
        return []
