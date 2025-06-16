import subprocess

def execute_terminal_command(command: str) -> str:
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"[Erro Terminal]: {e.output.decode('utf-8')}"
