from backend.agent.planner import Planner
from backend.interfaces.openai_client import OpenAIClient
from backend.tools.registry import call_tool_by_name

class Orchestrator:
    def __init__(self):
        self.planner = Planner()
        self.llm = OpenAIClient()

    def run(self, user_input: str) -> str:
        plan = self.planner.generate_plan(user_input)

        if not plan:
            return self.llm.complete_with_tools(user_input)

        results = []
        for step in plan:
            tool = step["tool"]
            args = step.get("args", {})
            result = call_tool_by_name(tool, args)
            results.append(f"[🔧 {tool}]\n{result}")

        return "\n\n".join(results)
