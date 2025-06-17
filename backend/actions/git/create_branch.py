import subprocess

def create_branch(branch_name: str) -> str:
    try:
        result = subprocess.run(["git", "checkout", "-b", branch_name], capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Branch criada: {branch_name}"
        return f"❌ Erro ao criar branch: {result.stderr.strip()}"
    except Exception as e:
        return f"[Erro] {str(e)}"
