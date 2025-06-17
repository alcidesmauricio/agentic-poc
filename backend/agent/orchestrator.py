import json
from backend.planner.rule_based import RuleBasedPlanner
from backend.tools.registry import call_tool_by_name

class Orchestrator:
    def __init__(self):
        self.planner = RuleBasedPlanner()

    def run(self, user_input):
        yield "[🤖] Gerando plano..."
        plan = self.planner.generate_plan(user_input)
        if not plan:
            yield "[⚠️] Nenhuma ação identificada para esse input."
            return

        yield f"[📋] Plano criado:\n{json.dumps(plan, indent=2)}"

        last_result = None

        for step in plan:
            tool = step["tool"]
            args = step["args"]

            # Substituição de __previous__ por resultado anterior
            for k, v in args.items():
                if isinstance(v, str) and "__previous__" in v:
                    args[k] = last_result or ""

        #   for key, value in args.items():
        #         if value == "__previous__":
        #             args[key] = result

            yield f"[⚙️] Executando: {tool}..."
            result = call_tool_by_name(tool, args)
            yield f"[✅] Resultado de {tool}:\n{result}"
            last_result = result