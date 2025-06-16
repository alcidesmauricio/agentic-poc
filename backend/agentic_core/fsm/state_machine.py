class StateMachine:
    def __init__(self):
        self.state = "idle"

    def process_event(self, event):
        # Lógica simples de transição de estados
        if "git" in event.lower():
            self.state = "git_analysis"
            return "Analisando estado do Git..."
        elif "terminal" in event.lower():
            self.state = "terminal_command"
            return "Pronto para executar comando de terminal."
        elif "file" in event.lower():
            self.state = "file_monitoring"
            return "Listando arquivos do projeto."
        else:
            self.state = "chat"
            return "Processando conversa geral com LLM."

state_machine = StateMachine()
