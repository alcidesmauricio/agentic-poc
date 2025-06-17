import subprocess

def get_git_status():
    try:
        result = subprocess.check_output(['git', 'status'], stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"[Erro Git Status]: {e.output.decode('utf-8')}"
