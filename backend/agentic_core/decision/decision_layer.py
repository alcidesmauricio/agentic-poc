from backend.agentic_core.llm_clients.openai_client import OpenAIClient

client = OpenAIClient()

def decide_and_act(user_input):
    return client.get_completion_with_tools(user_input)
