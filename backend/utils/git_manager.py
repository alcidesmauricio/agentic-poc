import subprocess

def git_status() -> str:
    try:
        return subprocess.check_output(["git", "status"]).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"[Erro Git Status]: {e.output.decode('utf-8')}"

def git_diff() -> str:
    try:
        return subprocess.check_output(["git", "diff"]).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"[Erro Git Diff]: {e.output.decode('utf-8')}"
