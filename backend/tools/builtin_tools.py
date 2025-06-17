from backend.tools.registry import register_tool
from backend.actions.git_actions.diff import get_git_diff
from backend.actions.git_actions.status import get_git_status
from backend.actions.git_actions.commit_changes import commit_changes
from backend.actions.git_actions.create_branch import create_branch
from backend.actions.git_actions.generate_commit_message import generate_commit_message
from backend.actions.git_actions.push_changes import push_changes
from backend.actions.terminal_actions import execute_terminal_command
from backend.actions.file_actions import list_project_files
from backend.actions.dev_tools import get_python_dependencies

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
    name="commit_changes",
    description="Realiza commit no repositório Git com uma mensagem.",
    parameters={
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "Mensagem do commit"
            }
        },
        "required": ["message"]
    }
)
def tool_commit_changes(message: str):
    return commit_changes(message)

@register_tool(
    name="create_branch",
    description="Cria uma nova branch no repositório Git.",
    parameters={
        "type": "object",
        "properties": {
            "branch_name": {
                "type": "string",
                "description": "Nome da nova branch"
            }
        },
        "required": ["branch_name"]
    }
)
def tool_create_branch(branch_name: str):
    return create_branch(branch_name)

@register_tool(
    name="generate_commit_message",
    description="Gera uma mensagem de commit baseada nas alterações.",
    parameters={}
)
def tool_generate_commit_message():
    return generate_commit_message()

@register_tool(
    name="push_changes",
    description="Realiza push das alterações para o repositório remoto.",
    parameters={}
)
def tool_push_changes():
    return push_changes()

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

@register_tool(
    name="get_python_dependencies",
    description="Lista os pacotes/dependências Python do projeto.",
    parameters={}
)
def tool_get_python_dependencies():
    return get_python_dependencies()