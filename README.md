# 🤖 stk AI DevAgentic — v2.2

Agente agentic de inteligência artificial para desenvolvedores, integrado ao VSCode.  
Comportamento proativo, linguagem natural, uso de ferramentas e percepção do ambiente.

---

## ✨ Funcionalidades principais

🧠 Planejamento baseado em linguagem natural  
🔁 FSM para estados de decisão e execução  
🧩 Execução de ferramentas com LLM Tool-Calling (OpenAI)  
🖥️ Integração WebSocket com extensão VSCode  
🧠 Memória de contexto de interações  
🔍 Observação reativa de terminal, arquivos e Git  
⚙️ Ferramentas nativas como git status, diff, terminal e arquivos  

---

## 📐 Arquitetura moderna (Mermaid)
mermaid
graph TD
  Client[VSCode Extension] -->|WebSocket| WebServer[FastAPI WebSocket Server]
  WebServer --> Orchestrator[Agent Orchestrator]
  Orchestrator --> Planner
  Orchestrator --> LLMClient[OpenAI Client]
  Orchestrator -->|Tool Calls| ToolRegistry
  ToolRegistry --> Tools[Built-in Tools]
  Tools --> GitTool
  Tools --> TerminalTool
  Tools --> FileTool
  Orchestrator --> Memory[Context Manager]
  GitWatcher --> Events
  FileWatcher --> Events
  TerminalWatcher --> Events

---

## 📂 Estrutura da Solução
backend/
├── agent/                  # Planner, Orchestrator, FSM
├── actions/                # Implementação de ações
├── events/                 # Observadores de eventos (Git, arquivos, terminal)
├── interfaces/             # Interface LLM e OpenAI client
├── memory/                 # Memória de contexto
├── tools/                  # Registro e execução de ferramentas (Tool-Calling)
├── utils/                  # Utilitários diversos
├── server/                 # WebSocket API
├── main.py                 # Ponto de entrada
vscode_extension/           # Extensão integrada com o VSCode

---

## ⚙️ Requisitos

Python 3.10+  
Node.js (para extensão VSCode)  
openai (Python SDK)  
Variável de ambiente OPENAI_API_KEY  

---

## 🚀 Como rodar

### Backend
bash
uvicorn backend.main:app --reload

### Extensão VSCode

1. Abra stk_ai_devagentic/vscode_extension no VSCode  
2. Pressione F5 para iniciar a extensão em modo dev  
3. Execute o comando Iniciar stk AI DevAgentic  

---

## 💬 Exemplos de comandos no chat

| Entrada do usuário                         | Ação executada                            |
|--------------------------------------------|-------------------------------------------|
| qual o status do git?                    | Tool: get_git_status()                  |
| mostre a diferença entre os arquivos     | Tool: get_git_diff()                    |
| execute o comando ls                     | Tool: run_terminal_command("ls")        |
| liste os arquivos do projeto             | Tool: list_project_files()              |
| explique esse código: + código           | LLM puro (sem tools)                      |

---

## 🤝 Contribuindo

Crie uma issue com sugestões ou bugs  
Envie PRs com novos watchers, FSMs, planners ou tools!  
Toda colaboração é bem-vinda 🙌  

---

## 📘 Licença

MIT — © 2025 stk AI DevAgentic.
