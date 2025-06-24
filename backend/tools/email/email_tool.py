def send_email_tool(subject: str, summary: str, destination: str):
    print(f"[📤] Enviando email para: {destination}")
    print(f"Assunto: {subject}")
    print(f"Resumo: {summary}")
    # Aqui você usaria uma API SMTP real ou outro meio
    return { "message": f"Email enviado para {destination}" }

def register():
    return [
        {
            "function": {
                "name": "send_email_tool",
                "description": "Envia um email com assunto e resumo para um destinatário",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "subject": { "type": "string" },
                        "summary": { "type": "string" },
                        "destination": { "type": "string" }
                    },
                    "required": ["subject", "summary", "destination"]
                }
            },
            "implementation": send_email_tool
        }
    ]
