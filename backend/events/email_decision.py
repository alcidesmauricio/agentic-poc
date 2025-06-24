from backend.interfaces.openai_client import OpenAIClient

def analyze_and_decide(email_data):
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    summary = summarize_email(email_data)

    llm = OpenAIClient()
    decision_prompt = f"""A seguir está o resumo de um e-mail:
    ---
    Assunto: {subject}
    Corpo: {body}
    Resumo: {summary}
    ---

    Decida o tipo de encaminhamento mais adequado com base no conteúdo. Retorne apenas:
    - "work" se for trabalho
    - "personal" se for pessoal
    - "ignore" se puder ser ignorado
    """

    response = llm.complete(decision_prompt).strip().lower()
    return {
        "summary": summary,
        "decision": response
    }

def summarize_email(email_data):
    llm = OpenAIClient()
    subject = email_data.get("subject", "")
    body = email_data.get("body", "")
    summary_prompt = f"Resuma o e-mail a seguir:\n\nAssunto: {subject}\n\nCorpo:\n{body}"
    response = llm.complete(summary_prompt).strip()
    return response
