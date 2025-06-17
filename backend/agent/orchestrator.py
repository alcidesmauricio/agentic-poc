from backend.planner import get_planner
from backend.tools.registry import call_tool_by_name
from backend.interfaces.openai_client import OpenAIClient

class Orchestrator:
    def __init__(self):
        self.planner = get_planner()
        self.llm_fallback = OpenAIClient()
   
    def run(self, user_input: str) -> str:
        plan = self.planner.generate_plan(user_input)
        result = None

        for step in plan:
            tool_name = step["tool"]
            args = step.get("args", {})

            # Substitui "__previous__" pelo resultado da etapa anterior
            for key, value in args.items():
                if value == "__previous__":
                    args[key] = result

            result = call_tool_by_name(tool_name, args)

        return result    