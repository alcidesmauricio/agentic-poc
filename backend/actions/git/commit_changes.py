import subprocess

def commit_changes(message: str) -> str:
    try:
        sanitized = message.replace('"', "'").strip()
        result = subprocess.run(["git", "commit", "-a", "-m", sanitized], capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Commit realizado com mensagem: {sanitized}"
        return f"❌ Erro ao realizar commit: {result.stderr.strip()}"
    except Exception as e:
        return f"[Erro] {str(e)}"