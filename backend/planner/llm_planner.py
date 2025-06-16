from typing import List, Dict
from backend.interfaces.llm_interface import LLMInterface
from .base import PlannerBase

class LLMPlanner(PlannerBase):
    def __init__(self, llm_client: LLMInterface):
        self.llm = llm_client

    def generate_plan(self, user_input: str) -> List[Dict]:
        system_prompt = "Você é um planejador de ações. Receba a intenção do usuário e retorne uma lista de ferramentas com argumentos a serem chamadas pelo agente."

        prompt = f"""
Usuário: "{user_input}"

Retorne um plano em formato JSON, ex:
[
  {{ "tool": "get_git_status", "args": {{}} }},
  {{ "tool": "commit_changes", "args": {{ "message": "commit inicial" }} }}
]
        """.strip()

        response = self.llm.chat(system=system_prompt, user=prompt)

        try:
            plan = eval(response)
            if isinstance(plan, list):
                return plan
        except Exception:
            pass

        return []
