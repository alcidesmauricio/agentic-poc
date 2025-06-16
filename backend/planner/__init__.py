from .rule_based import RuleBasedPlanner
try:
    from .llm_planner import LLMPlanner
    from backend.interfaces.openai_client import OpenAIClient
    llm_client = OpenAIClient()
    planner = LLMPlanner(llm_client)
except:
    planner = RuleBasedPlanner()

get_planner = lambda: planner
