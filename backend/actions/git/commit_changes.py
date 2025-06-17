import subprocess

def commit_changes(message: str) -> str:
    try:
        result = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Commit realizado com mensagem: {message}"
        return f"❌ Erro ao realizar commit: {result.stderr.strip()}"
    except Exception as e:
        return f"[Erro] {str(e)}"
