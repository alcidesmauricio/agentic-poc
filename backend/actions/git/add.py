import subprocess

def git_add():
    try:
        result = subprocess.check_output(['git', 'add', '.'], stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"[Erro Git Add]: {e.output.decode('utf-8')}"
