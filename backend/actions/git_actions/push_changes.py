import subprocess

def push_changes() -> str:
    try:
        result = subprocess.run(["git", "push"], capture_output=True, text=True)
        if result.returncode == 0:
            return "✅ Push realizado com sucesso."
        return f"❌ Erro ao fazer push: {result.stderr.strip()}"
    except Exception as e:
        return f"[Erro] {str(e)}"
