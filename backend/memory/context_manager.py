class ContextManager:
    def __init__(self):
        self.context = []

    def add_message(self, role: str, content: str):
        """Armazena uma mensagem no contexto (user ou assistant)"""
        self.context.append({"role": role, "content": content})

    def get_context(self):
        """Retorna os últimos N elementos do histórico"""
        return self.context[-10:]

    def clear(self):
        """Limpa todo o histórico"""
        self.context = []
