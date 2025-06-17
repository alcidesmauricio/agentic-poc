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
        response = self.llm.complete(prompt).strip()

        if not response:
            print("❌ LLM retornou resposta vazia.")
            return []

        try:
            plan = json.loads(response)
            if not isinstance(plan, list):
                raise ValueError("JSON não é uma lista de passos.")
            return plan
        except Exception as e:
            print(f"❌ Erro ao fazer json.loads(): {e}")
            print(f"🔁 Conteúdo bruto da LLM:\n{response}")
            return []

    def build_prompt(self, user_input: str, history: List[Dict]) -> str:
        tools = get_registered_tools()
        tool_names = [tool["function"]["name"] for tool in tools]

        history_str = "\n".join(
            [f"[🔧{step.get('tool')}]: {step.get('result', '...')}" for step in history]
        ) or "Nenhum histórico disponível."

        prompt = f"""
        Você é um planejador de ações para um agente de desenvolvimento.

        Seu papel é analisar o pedido do usuário e, com base nas ferramentas disponíveis e no histórico recente de execuções, decidir **quais ferramentas devem ser chamadas e com quais argumentos**.

        ---

        🎯 Objetivo do usuário:
        {user_input}

        📚 Histórico de execuções anteriores:
        {history_str}

        🔧 Ferramentas disponíveis:
        {tool_names}

        ---

        📝 Sua tarefa:

        1. Liste as próximas ações a serem executadas, utilizando até **3 ferramentas**, no seguinte formato:

        [
          {{ "tool": "nome_da_tool", "args": {{ ... }} }},
          ...
        ]

        2. Se **nenhuma ação for necessária**, retorne um JSON vazio: [].

        3. Se o pedido for muito genérico ou amplo (ex: "em que você pode me ajudar?"), utilize ferramentas como get_git_status, list_files, etc., para **coletar contexto antes de decidir**.

        4. Evite executar ações irrelevantes. Seja pragmático.

        ⚠️ IMPORTANTE:

        - **Retorne apenas um JSON válido**, diretamente parsável com json.loads().
        - Não inclua comentários, explicações, markdown, prefixos como "json", nem texto fora do JSON.
        - Use **aspas duplas** em nomes e valores de chave (ex: "tool", "args").
        - Não deixe vírgulas no final de listas ou objetos.

        Exemplo válido:
        [
          {{ "tool": "get_git_status", "args": {{}} }},
          {{ "tool": "commit_files", "args": {{ "message": "Ajustes finais" }} }}
        ]
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