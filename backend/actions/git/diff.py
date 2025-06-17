import subprocess

def get_git_diff() -> dict:
    try:
        result = subprocess.run(['git', 'diff', '--cached'], capture_output=True, text=True)
        diff = result.stdout.strip()
        if not diff:
            return {
                "message": "[🟡] Nenhuma alteração staged encontrada.",
                "skip_commit": True
            }
        return {
            "diff": diff,
            "skip_commit": False
        }
    except Exception as e:
        return { "message": f"[Erro Git Diff]: {e}", "skip_commit": True }