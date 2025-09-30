from mcp.server.fastmcp import FastMCP
import subprocess

# Criar servidor MCP
mcp = FastMCP("ToolServer")

# Tool que executa git status
@mcp.tool()
def git_status() -> str:
    """Executa 'git status' no diretório atual"""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)


@mcp.tool()
def git_status() -> str:
    """Executa 'git status' no diretório atual"""
    try:
        result = subprocess.run(["git", "status"], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)


# Iniciar o servidor
if __name__ == "__main__":
    mcp.run(transport="stdio")
