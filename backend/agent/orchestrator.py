import json
from backend.tools.registry import call_tool_by_name
from backend.interfaces.openai_client import OpenAIClient
from backend.planner.llm_planner import LLMPlanner
from backend.planner.rule_based import RuleBasedPlanner

class Orchestrator:
    def __init__(self, mode="rule"):
        self.mode = mode
        self.replanning_enabled = True
        self.llm = OpenAIClient()

    def run(self, user_input: str):
        print(f"🧠 Modo do planner: {self.mode}")
        planner = LLMPlanner() if self.mode == "llm" else RuleBasedPlanner()


        # Histórico pode ser carregado de uma memória futura; por ora, vazio:
        history = []

        plan = planner.generate_plan(user_input, history)

        yield f"json\n📋 Plano gerado:\n{json.dumps(plan, indent=2)}\n"

        previous_result = None
        for step in plan:
            tool_name = step["tool"]
            args = step.get("args", {})

            for k, v in args.items():
                if isinstance(v, str) and v == "__previous__":
                    args[k] = previous_result

            yield f"bash\n⚙️ Executando: {tool_name}...\n"
            result = call_tool_by_name(tool_name, args)

            if isinstance(result, dict) and result.get("skip_commit"):
                yield f"bash\n⏭️ Pulando etapa: {tool_name} – {result['message']}\n"

                if self.replanning_enabled:
                    yield f"bash\n🔁 Replanejando com base no resultado anterior...\n"
                    plan = planner.generate_plan(result["message"])

                    if not plan or "commit" in result["message"].lower():
                        yield f"bash\n✅ Commit abortado por ausência de alterações. Nenhuma ação será executada.\n"
                        return

                    yield f"json\n🆕 Novo plano:\n{json.dumps(plan, indent=2)}\n"
                    previous_result = None
                    continue

            previous_result = result.get("message", result) if isinstance(result, dict) else result
            yield f"json\n✅ Resultado de {tool_name}:\n{previous_result}\n"