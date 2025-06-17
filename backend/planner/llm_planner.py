from backend.planner.base import PlannerBase
from backend.interfaces.openai_client import OpenAIClient
from typing import List, Dict

class LLMPlanner(PlannerBase):
    def generate_plan(self, user_input: str, history: List[Dict] = []) -> List[Dict]:
        prompt = self.build_prompt(user_input, history)
        llm = OpenAIClient()
        response = llm.complete(prompt)
        return self.parse_steps(response)

    def build_prompt(self, user_input: str, history: List[Dict]) -> str:
        history_str = "\n".join(
            f"[{step['tool']}]: {step.get('result', '...')}" for step in history
        )
        return f"""Você é um planejador de ações para um agente de desenvolvimento.
Baseado no objetivo do usuário e nos resultados anteriores, decida quais ferramentas executar em seguida.

Objetivo do usuário: "{user_input}"

Histórico de execuções anteriores:
{history_str}

Liste as próximas ferramentas a executar (máximo 3), no formato:
tool: <nome_da_tool>, args: {{ ... }}
"""

    def parse_steps(self, response: str) -> List[Dict]:
        steps = []
        for line in response.strip().split("\n"):
            if "tool:" in line:
                tool = line.split("tool:")[1].split(",")[0].strip()
                args_part = line.split("args:")[1].strip()
                args = eval(args_part) if args_part.startswith("{") else {}
                steps.append({ "tool": tool, "args": args })
        return steps
