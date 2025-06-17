from backend.interfaces.openai_client import OpenAIClient

def generate_commit_message(diff: str) -> dict:
    prompt = f"""Você é um assistente de desenvolvimento.
Baseado no seguinte diff de código, gere uma mensagem de commit clara e objetiva:

{diff}
"""
    try:
        llm = OpenAIClient()
        message = llm.complete(prompt)
        return { "message": message }
    except Exception as e:
        return { "message": f"[Erro]: {str(e)}" }