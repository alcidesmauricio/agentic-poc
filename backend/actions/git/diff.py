import subprocess

def get_git_diff():
    try:
        result = subprocess.check_output(['git', 'diff'], stderr=subprocess.STDOUT)
        return result.decode('utf-8') or "[Sem alterações]"
    except subprocess.CalledProcessError as e:
        return f"[Erro Git Diff]: {e.output.decode('utf-8')}"
