from typing import List, Dict

class Planner:
    def __init__(self):
        pass

    def generate_plan(self, user_input: str) -> List[Dict]:
        plan = []

        if "status" in user_input:
            plan.append({"tool": "get_git_status", "args": {}})
        elif "diff" in user_input:
            plan.append({"tool": "get_git_diff", "args": {}})
        elif "listar arquivos" in user_input.lower():
            plan.append({"tool": "list_project_files", "args": {}})
        elif "executa" in user_input or "comando" in user_input:
            plan.append({"tool": "run_terminal_command", "args": {"command": "ls"}})

        return plan
