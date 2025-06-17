from typing import List, Dict
from .base import PlannerBase
from backend.planner.base import PlannerBase
from typing import List, Dict

class RuleBasedPlanner(PlannerBase):
    def generate_plan(self, user_input: str, history: List[Dict] = []) -> List[Dict]:
        plan = []
        lower = user_input.lower()


        if "add" in lower:
            plan.append({ "tool": "git_add", "args": {} })
        elif "status" in lower:
            plan.append({ "tool": "get_git_status", "args": {} })
        elif "diff" in lower or "alterações" in lower:
            plan.append({ "tool": "get_git_diff", "args": {} })
        elif "listar arquivos" in lower or "lista os arquivos" in lower:
            plan.append({ "tool": "list_project_files", "args": {} })
        elif "executa" in lower or "comando" in lower:
            plan.append({ "tool": "run_terminal_command", "args": { "command": "ls" } })
        elif "mensagem de commit" in lower:
            plan.append({ "tool": "get_git_diff", "args": {} })
            plan.append({ "tool": "generate_commit_message", "args": { "diff": "__previous__" } })
        elif "commit tudo" in lower:
            plan.append({ "tool": "git_add", "args": {} })            
            plan.append({ "tool": "get_git_diff", "args": {} })
            plan.append({ "tool": "generate_commit_message", "args": { "diff": "__previous__" } })
            plan.append({ "tool": "commit_changes", "args": { "message": "__previous__" } })
            plan.append({ "tool": "push_changes", "args": {} })
        elif "commit" in lower:
            plan.append({ "tool": "commit_changes", "args": { "message": "commit gerado automaticamente" } })
        elif "branch" in lower:
            plan.append({ "tool": "create_branch", "args": { "name": "nova-branch" } })
        elif "push" in lower:
            plan.append({ "tool": "push_changes", "args": {} })
        elif "dependência" in lower or "pacote" in lower:
            plan.append({ "tool": "get_python_dependencies", "args": {} })
        elif "buscar" in lower or "procurar" in lower:
            plan.append({ "tool": "search_in_files", "args": { "keyword": "TODO" } })
        elif "porta" in lower:
            plan.append({ "tool": "check_port_usage", "args": { "port": 8000 } })
        elif "linhas" in lower or "resumo" in lower:
            plan.append({ "tool": "get_file_summary", "args": { "filepath": "README.md" } })

        return plan

