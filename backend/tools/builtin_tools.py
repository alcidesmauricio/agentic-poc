from backend.tools.registry import register_tool
from backend.actions.git.add import git_add
from backend.actions.git.diff import get_git_diff
from backend.actions.git.status import get_git_status
from backend.actions.git.commit_changes import commit_changes
from backend.actions.git.create_branch import create_branch
from backend.actions.git.generate_commit_message import generate_commit_message
from backend.actions.git.push_changes import push_changes
from backend.actions.terminal_actions import execute_terminal_command
from backend.actions.file_actions import list_project_files
from backend.actions.dev_tools import get_python_dependencies
from backend.tools.agent_router import agent_router_tool
from typing import List

@register_tool(
    name="git_add",
    description="Executa o add no repositório Git.",
    parameters={}
)
def tool_git_add():
    return git_add()


@register_tool(
    name="get_git_status",
    description="Mostra o status atual do repositório Git.",
    parameters={}
)
def tool_get_git_status():
    return get_git_status()

@register_tool(
    name="get_git_diff",
    description="Verifica alterações staged no repositório Git. Retorna o conteúdo do diff e indica se o commit deve ser pulado.",
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
    description="Gera uma mensagem de commit com base no diff.",
    parameters={
        "type": "object",
        "properties": {
            "diff": {
                "type": "string",
                "description": "Conteúdo do diff Git"
            }
        },
        "required": ["diff"]
    }
)
def tool_generate_commit_message(diff: str):
    return generate_commit_message(diff)

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

@register_tool(
    name="agent_router",
    description="Roteia a solicitação do usuário para o agente apropriado com base no contexto ou delega a um agente master.",
    parameters={
        "type": "object",
        "properties": {
            "input_text": {
                "type": "string",
                "description": "Texto da solicitação do usuário."
            },
            "master_agent": {
                "type": "string",
                "description": "Nome do agente master que tomará a decisão sobre qual filho chamar."
            },
            "child_agents": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "Lista de agentes filhos disponíveis."
            }
        },
        "required": ["input_text", "master_agent"]  # <-- Corrigido!
    }
)
async def tool_agent_router(input_text: str, master_agent: str = None, child_agents: List[str] = None):
    return await agent_router_tool(input_text, master_agent, child_agents)