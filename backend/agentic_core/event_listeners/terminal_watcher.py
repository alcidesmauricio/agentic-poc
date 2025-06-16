def listen_terminal_event(command_output):
    if "error" in command_output.lower():
        return "⚠️ Detectado erro no terminal."
    return "✅ Comando executado com sucesso."
