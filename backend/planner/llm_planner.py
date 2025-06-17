import json
from typing import List, Dict
from backend.planner.base import PlannerBase
from backend.interfaces.openai_client import OpenAIClient
from backend.tools.registry import get_registered_tools
from backend.tools.registry import get_registered_tools


class LLMPlanner(PlannerBase):
    def __init__(self):
        self.llm = OpenAIClient()

    def generate_plan(self, user_input: str, history: List[Dict] = []) -> List[Dict]:
        prompt = self.build_prompt(user_input, history)
        response = self.llm.complete(prompt)

        if not response or not response.strip():
            print("⚠️ LLM retornou resposta vazia.")
            return []

        # Limpa prefixos como "json\n"
        response_clean = response.strip()
        if response_clean.lower().startswith("json"):
            response_clean = response_clean[4:].strip()

        try:
            plan = json.loads(response_clean)
            if not isinstance(plan, list):
                raise ValueError("❌ JSON não é uma lista de steps.")
            return plan
        except json.JSONDecodeError as e:
            print("❌ Erro ao fazer json.loads():", e)
            print("🔁 Conteúdo bruto da LLM (limpo):", response_clean)
            return []
        except Exception as e:
            print("❌ Erro inesperado no parsing:", e)
            return []

    def build_prompt(self, user_input: str, history: List[Dict]) -> str:
        tools = get_registered_tools()
        tool_names = [tool["function"]["name"] for tool in tools]

        history_str = "\n".join(
            [f"[🔧{step.get('tool')}]: {step.get('result', '...')}" for step in history]
        )        

        prompt = f"""
        Você é um planejador de ações para um agente de desenvolvimento.

        Baseado no objetivo do usuário e nos resultados anteriores, decida quais ferramentas devem ser executadas em seguida.

        Objetivo do usuário:
        {user_input}

        Histórico de execuções anteriores:
        {history_str}

        Ferramentas disponíveis:
        {tool_names}

        Retorne APENAS um JSON VÁLIDO com a lista de passos a seguir, no seguinte formato:

        [
        {{ "tool": "nome_da_tool", "args": {{ ... }} }},
        ...
        ]

        ⚠️ IMPORTANTE:
        O retorno deve ser um JSON válido e parsável com json.loads().
        NÃO adicione nenhum comentário, explicação ou texto fora do JSON.
        Utilize aspas duplas em nomes e valores de chave (ex: "tool", "args").
        Evite deixar vírgulas sobrando no final de listas ou objetos.
        Não escreva a palavra “json” antes. Retorne apenas o JSON.
        """
        return prompt.strip()

    def parse_steps(self, response: str) -> List[Dict]:
        steps = []
        for line in response.strip().split("\n"):
            if "tool" in line:
                try:
                    tool = line.split("tool:")[1].split(",")[0].strip()
                    args_str = line.split("args:")[1].strip()
                    args = eval(args_str) if args_str.startswith("{") else {}
                    steps.append({ "tool": tool, "args": args })
                except Exception as e:
                    print(f"[⚠️ Erro ao interpretar linha]: {line}\n{e}")
        return steps