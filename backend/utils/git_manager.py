import os
from git import Repo, GitCommandError

def get_repo():
    try:
        repo = Repo('.', search_parent_directories=True)
        if repo.bare:
            raise Exception("Repositório Git não encontrado.")
        return repo
    except Exception as e:
        return None

def get_status():
    repo = get_repo()
    if not repo:
        return "Repositório Git não encontrado."
    try:
        return repo.git.status()
    except GitCommandError as e:
        return f"Erro ao obter status do Git: {str(e)}"

def get_diff():
    repo = get_repo()
    if not repo:
        return "Repositório Git não encontrado."
    try:
        return repo.git.diff()
    except GitCommandError as e:
        return f"Erro ao obter diff do Git: {str(e)}"
