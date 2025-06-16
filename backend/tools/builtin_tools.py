from backend.tools.registry import register_tool
from backend.actions.git_actions import get_git_status, get_git_diff
from backend.actions.terminal_actions import execute_terminal_command
from backend.actions.file_actions import list_project_files

@register_tool(
    name="get_git_status",
    description="Mostra o status atual do repositório Git.",
    parameters={}
)
def tool_get_git_status():
    return get_git_status()

@register_tool(
    name="get_git_diff",
    description="Exibe as alterações não commitadas no repositório Git.",
    parameters={}
)
def tool_get_git_diff():
    return get_git_diff()

@register_tool(
    name="run_terminal_command",
    description="Executa um comando de terminal.",
    parameters={
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "Comando a ser executado"
            }
        },
        "required": ["command"]
    }
)
def tool_run_terminal_command(command: str):
    return execute_terminal_command(command)

@register_tool(
    name="list_project_files",
    description="Lista todos os arquivos do projeto (exceto .git).",
    parameters={}
)
def tool_list_project_files():
    return list_project_files()
