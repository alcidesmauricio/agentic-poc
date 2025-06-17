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

            # Substituir __previous__ pelo resultado anterior
            for k, v in args.items():
                if isinstance(v, str) and v == "__previous__":
                    args[k] = previous_result

            yield f"[⚙️ Executando: {tool_name}...]"
            result = call_tool_by_name(tool_name, args)

            # Replanejar se ferramenta sinalizar
            if isinstance(result, dict):
                if result.get("skip_commit"):
                    yield f"[⏩ Pulando etapa: {tool_name}] → {result['message']}"
                    if self.replanning_enabled:
                        yield "[🔁 Replanejando com base no resultado anterior...]"
                        plan = planner.generate_plan(result["message"])
                        yield f"[📋 Novo plano]:\n{json.dumps(plan, indent=2)}"
                        previous_result = None
                        continue  # Recomeça com o novo plano

            previous_result = result.get("message", result) if isinstance(result, dict) else result
            yield f"[✅ Resultado de {tool_name}]:\n{previous_result}"
