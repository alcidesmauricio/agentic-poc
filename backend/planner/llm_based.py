import json
from backend.interfaces.llm_interface import LLMInterface
from backend.interfaces.openai_client import OpenAIClient
from backend.tools.registry import get_registered_tools

class LLMPlanner:
    def __init__(self):
        self.llm = LLMInterface()

    def generate_plan(self, user_input: str) -> list[dict]:
        tools = get_registered_tools()
        tool_names = [tool["name"] for tool in tools]

        prompt = f"""
Você é um planejador de ações para um agente de desenvolvimento. Com base no pedido abaixo, gere um plano em JSON.

Pedido do usuário:
{user_input}

Ferramentas disponíveis:
{tool_names}

Formato esperado:
[
  {{ "tool": "nome_da_tool", "args": {{...}} }},
  ...
]
"""

        plan_str = self.llm.complete(prompt)
        return json.loads(plan_str)
