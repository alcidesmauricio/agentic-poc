# server.py
# Requisitos: pip install "mcp[cli]"
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-git")

def run_git(args: List[str], cwd: Path) -> Tuple[int, str, str]:
    p = subprocess.Popen(
        ["git"] + args,
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    out, err = p.communicate()
    return p.returncode, out.strip(), err.strip()

def resolve_repo_root(start: Path) -> Path:
    # git rev-parse --show-toplevel resolve o root do repositório
    code, out, err = run_git(["rev-parse", "--show-toplevel"], start)
    if code != 0:
        raise RuntimeError(f"Não é um repo Git: {start} ({err})")
    return Path(out)

def parse_porcelain(lines: List[str]) -> Dict[str, List[str]]:
    staged, modified, untracked = [], [], []
    for line in lines:
        if not line:
            continue
        # Porcelain v1: XY path
        # untracked começa com "??"
        if line.startswith("?? "):
            untracked.append(line[3:].strip())
            continue
        # Demais: 2 colunas de status + espaço + path
        if len(line) >= 3:
            x, y = line[0], line[1]
            path = line[3:].strip()
            if x != " " and x != "?":
                staged.append(path)
            if y != " ":
                modified.append(path)
    return {"staged": staged, "modified": modified, "untracked": untracked}

def ahead_behind(repo_root: Path, branch_line: str) -> Tuple[int, int, str]:
    """
    branch_line vem do --porcelain=v1 --branch (ex.: '## main...origin/main [ahead 1, behind 2]')
    Retorna (ahead, behind, branch_name).
    """
    branch_name = "(detached)"
    ahead = behind = 0
    # branch_line começa com '## '
    meta = branch_line[3:].strip() if branch_line.startswith("## ") else branch_line.strip()
    # Ex.: 'main', 'main...origin/main [ahead 1]', etc.
    # branch name é antes do primeiro '.' ou espaço
    if "..." in meta:
        branch_name = meta.split("...")[0]
    else:
        branch_name = meta.split()[0]

    # tenta extrair [ahead X, behind Y]
    if "[" in meta and "]" in meta:
        bracket = meta[meta.index("[")+1: meta.index("]")]
        parts = [p.strip() for p in bracket.split(",")]
        for p in parts:
            if p.startswith("ahead "):
                try:
                    ahead = int(p.split("ahead ")[1])
                except ValueError:
                    pass
            if p.startswith("behind "):
                try:
                    behind = int(p.split("behind ")[1])
                except ValueError:
                    pass
    return ahead, behind, branch_name

@mcp.tool(name="git.status")
def git_status(repo_path: Optional[str] = None) -> dict:
    """
    Retorna o status do repositório Git:
    - repo_root
    - branch
    - ahead / behind
    - staged / modified / untracked
    - is_dirty
    """
    cwd = Path(repo_path or ".").resolve()
    repo_root = resolve_repo_root(cwd)

    # Porcelain com branch info
    code, out, err = run_git(["status", "--porcelain=v1", "--branch", "--renames"], repo_root)
    if code != 0:
        raise RuntimeError(f"git status falhou: {err}")

    lines = out.splitlines()
    branch_info = next((l for l in lines if l.startswith("## ")), "## (detached)")
    file_lines = [l for l in lines if not l.startswith("## ")]

    changes = parse_porcelain(file_lines)
    ahead, behind, branch = ahead_behind(repo_root, branch_info)

    # dirty: qualquer staged/modified/untracked
    is_dirty = any(changes[k] for k in ("staged", "modified", "untracked"))

    return {
        "repo_root": str(repo_root),
        "branch": branch,
        "ahead": ahead,
        "behind": behind,
        "staged": changes["staged"],
        "modified": changes["modified"],
        "untracked": changes["untracked"],
        "is_dirty": is_dirty,
    }


#dfggfdgf
if __name__ == "__main__":
    # Para rodar local conectado a um client MCP (ex. VS Code host/Claude Desktop), use transporte stdio:
    mcp.run(transport="stdio")
