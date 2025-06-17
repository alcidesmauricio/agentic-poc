from backend.interfaces.openai_client import OpenAIClient

def generate_commit_message(diff: str) -> dict:
    if not diff.strip():
        return {
            "message": "[🛑] Nenhuma alteração detectada. Abortando commit.",
            "skip_commit": True
        }

    prompt = f"""
Você é um assistente de desenvolvimento.
Com base no seguinte diff de código, gere uma mensagem de commit curta, clara e descritiva:

{diff}
"""

    try:
        llm = OpenAIClient()
        message = llm.complete(prompt)
        return { "message": message, "skip_commit": False }
    except Exception as e:
        return { "message": f"[Erro]: {str(e)}", "skip_commit": True }
