from backend.planner import get_planner
from backend.tools.registry import call_tool_by_name

class Orchestrator:
    def __init__(self):
        self.planner = get_planner()

    def run(self, user_input: str) -> str:
        plan = self.planner.generate_plan(user_input)

        if not plan:
            return "Nenhuma ação identificada para esse input."

        results = []
        for step in plan:
            tool = step.get("tool")
            args = step.get("args", {})
            result = call_tool_by_name(tool, args)
            results.append(f"[🔧 {tool}] {result}")

        return "\n".join(results)
