from backend.interfaces.openai_client import OpenAIClient
from backend.actions.git_actions.diff import get_git_diff
def generate_commit_message() -> str:
    try:
        result = get_git_diff()
        diff = result

        if not diff.strip():
            return "[🤖] Nenhuma alteração staged encontrada."

        prompt = f"""Você é um assistente de desenvolvimento.
Com base no seguinte diff de código, gere uma mensagem de commit curta, clara e descritiva, no estilo convencional:

{diff}
"""

        llm = OpenAIClient()
        return llm.complete(prompt)

    except Exception as e:
        return f"[Erro]: {str(e)}"