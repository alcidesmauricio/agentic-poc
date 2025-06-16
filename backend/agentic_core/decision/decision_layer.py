from backend.agentic_core.actions import git_actions, terminal_actions, file_actions

def decide_and_act(user_input):
    if "status do git" in user_input.lower():
        return git_actions.get_git_status()
    elif "diff" in user_input.lower():
        return git_actions.get_git_diff()
    elif "executar comando" in user_input.lower():
        command = user_input.replace("executar comando", "").strip()
        return terminal_actions.execute_terminal_command(command)
    elif "listar arquivos" in user_input.lower():
        return file_actions.list_project_files()
    else:
        return "Não entendi a solicitação."
