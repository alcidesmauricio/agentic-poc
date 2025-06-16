from typing import List, Dict
from .base import PlannerBase

class RuleBasedPlanner(PlannerBase):
    def generate_plan(self, user_input: str) -> List[Dict]:
        plan = []
        input_lower = user_input.lower()

        if "status" in input_lower:
            plan.append({"tool": "get_git_status", "args": {}})
        elif "diff" in input_lower:
            plan.append({"tool": "get_git_diff", "args": {}})
        elif "listar arquivos" in input_lower or "lista de arquivos" in input_lower:
            plan.append({"tool": "list_project_files", "args": {}})
        elif "executa" in input_lower or "comando" in input_lower:
            plan.append({"tool": "run_terminal_command", "args": {"command": "ls"}})

        return plan
