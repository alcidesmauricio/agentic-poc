from backend.planner import get_planner
from backend.tools.registry import call_tool_by_name
from backend.interfaces.openai_client import OpenAIClient

class Orchestrator:
    def __init__(self):
        self.planner = get_planner()
        self.llm_fallback = OpenAIClient()

    def run(self, user_input: str) -> str:
        plan = self.planner.generate_plan(user_input)

        # ✅ Fallback se nenhuma ação for identificada
        if not plan:
            return self.llm_fallback.complete(user_input)

        results = []
        for step in plan:
            tool = step.get("tool", "")
            args = step.get("args", {})
            result = call_tool_by_name(tool, args)
            results.append(f"[🔧 {tool}] {result}")

        return "\n\n".join(results)