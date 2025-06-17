from backend.interfaces.openai_client import OpenAIClient

def generate_commit_message(diff: str) -> str:
    if not diff.strip():
        return "[🧼] Nenhuma alteração staged encontrada."

    prompt = f"""
    Você é um assistente de desenvolvimento.
    Com base no seguinte diff de código, gere uma mensagem de commit curta, clara e descritiva:

    {diff}
    """
    try:
        llm = OpenAIClient()
        return llm.complete(prompt)
    except Exception as e:
        return f"[Erro]: {str(e)}"