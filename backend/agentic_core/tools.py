from backend.agentic_core.actions import git_actions, terminal_actions, file_actions

tool_specs = [
    {
        "type": "function",
        "function": {
            "name": "get_git_status",
            "description": "Retorna o status do repositório Git",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_git_diff",
            "description": "Retorna as alterações atuais do Git (git diff)",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_terminal_command",
            "description": "Executa um comando no terminal",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "O comando a ser executado"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_project_files",
            "description": "Lista todos os arquivos do projeto",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

tool_implementations = {
    "get_git_status": lambda: git_actions.get_git_status(),
    "get_git_diff": lambda: git_actions.get_git_diff(),
    "run_terminal_command": lambda command: terminal_actions.execute_terminal_command(command),
    "list_project_files": lambda: "\n".join(file_actions.list_project_files())
}
