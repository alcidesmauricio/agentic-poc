import os
import socket
import subprocess
from backend.tools.registry import register_tool

@register_tool(
    name="search_in_files",
    description="Busca uma palavra-chave em todos os arquivos do projeto.",
    parameters={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "Palavra-chave a ser buscada"
            }
        },
        "required": ["keyword"]
    }
)
def search_in_files(keyword: str) -> str:
    result = []
    for root, _, files in os.walk("."):
        for file in files:
            if ".git" in root:
                continue
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    for i, line in enumerate(f):
                        if keyword in line:
                            result.append(f"{path}:{i+1}: {line.strip()}")
            except Exception:
                continue
    return "\n".join(result) or "[🔍] Nenhum resultado encontrado."

@register_tool(
    name="get_python_dependencies",
    description="Lista os pacotes Python usados no projeto, com fallback automático.",
    parameters={}
)
def get_python_dependencies() -> str:
    try:
        if os.path.exists("requirements.txt"):
            with open("requirements.txt", "r", encoding="utf-8") as f:
                content = f.read().strip()
                return content or "[📦] requirements.txt está vazio."
        else:
            import subprocess
            output = subprocess.check_output(["pip", "freeze"], text=True)
            return output.strip() or "[📦] Nenhuma dependência instalada com pip."
    except Exception as e:
        return f"[Erro]: {e}"

@register_tool(
    name="check_port_usage",
    description="Verifica se uma porta está em uso.",
    parameters={
        "type": "object",
        "properties": {
            "port": {
                "type": "integer",
                "description": "Porta a ser verificada"
            }
        },
        "required": ["port"]
    }
)
def check_port_usage(port: int) -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("localhost", port))
    sock.close()
    return f"[📡] Porta {port} está {'ocupada' if result == 0 else 'livre'}."

@register_tool(
    name="get_file_summary",
    description="Mostra as primeiras linhas de um arquivo.",
    parameters={
        "type": "object",
        "properties": {
            "filepath": {
                "type": "string",
                "description": "Caminho para o arquivo"
            }
        },
        "required": ["filepath"]
    }
)
def get_file_summary(filepath: str) -> str:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = [next(f).rstrip() for _ in range(10)]
        return "\n".join(lines)
    except Exception as e:
        return f"[Erro]: {e}"

@register_tool(
    name="create_and_run_python_file",
    description="Cria um arquivo .py e executa o conteúdo.",
    parameters={
        "file_name": {"type": "string", "description": "Nome do arquivo a ser criado."},
        "content": {"type": "string", "description": "Código Python a ser escrito e executado."}
    }
)
def create_and_run_python_file(file_name: str, content: str) -> dict:
    try:
        with open(file_name, "w") as f:
            f.write(content)

        result = subprocess.run(
            ["python3", file_name],
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            "message": result.stdout or result.stderr,
            "success": result.returncode == 0
        }

    except Exception as e:
        return {
            "message": f"Erro ao criar ou executar: {str(e)}",
            "success": False
        }