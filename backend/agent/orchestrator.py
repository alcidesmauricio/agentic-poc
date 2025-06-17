import json
from backend.tools.registry import get_registered_tools, call_tool_by_name
from backend.interfaces.llm_interface import LLMInterface
from backend.interfaces.openai_client import OpenAIClient
class Orchestrator:
    def __init__(self):
        self.llm = OpenAIClient()
        self.replanning_enabled = True

    def run(self, user_input: str):
        from backend.planner.rule_based import RuleBasedPlanner
        planner = RuleBasedPlanner()
        plan = planner.generate_plan(user_input)
        yield f"[📋 Plano gerado]:\n{json.dumps(plan, indent=2)}"

        previous_result = None
        for i, step in enumerate(plan):
            tool_name = step["tool"]
            args = step.get("args", {})
            for k, v in args.items():
                if v == "__previous__":
                    args[k] = previous_result or ""

            yield f"[⚙️ Executando: {tool_name}...]"
            result = call_tool_by_name(tool_name, args)
            yield f"[✅ Resultado de {tool_name}]:\n{result}"
            previous_result = result

            if self.replanning_enabled:
                new_plan = self.llm_replan(user_input, result, tool_name, plan[i+1:])
                if new_plan:
                    yield "[🔁 Replanner ativado: novo plano gerado]"
                    plan = plan[:i+1] + new_plan

    def llm_replan(self, user_input, last_result, last_tool, remaining_plan):
        prompt = f"""
Você é um agente inteligente com autonomia para ajustar o plano de execução.

Usuário pediu: "{user_input}"

Última ferramenta executada: "{last_tool}"
Resultado: "{last_result}"

Plano restante: {json.dumps(remaining_plan)}

Você deve:
❌ Cancelar etapas inúteis se o resultado indicar que elas não são mais necessárias
✅ Reescrever o plano a partir daqui apenas se necessário
✅ Se não for necessário replanejar, responda apenas: "CONTINUE"

Novo plano (formato JSON): 
"""
        new_plan_raw = self.llm.complete(prompt)
        if "CONTINUE" in new_plan_raw.upper():
            return None
        try:
            return json.loads(new_plan_raw)
        except Exception:
            return None
