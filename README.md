# AI DevAgentic — v2.2

Agentic AI agent para desenvolvedores, com suporte inicial para VSCode e backend Core.  
Comportamento proativo, linguagem natural, uso de ferramentas e percepção do ambiente.

---

## Funcionalidades principais

- Planejamento dinâmico com LLM (via tool-calling) ou heurística baseada em regras  
- FSM e Decision Layer para estados de raciocínio e execução  
- Tool Registry com execução segura e extensível (LLM Tool-Calling)  
- Extensão WebSocket para VSCode com chat em tempo real  
- Watchers de arquivos e Git integrados ao ciclo do agente  
- Ferramentas internas: Git Tool, File Tool, Terminal Tool, Python Runner Tool  
- Memória de contexto local (em desenvolvimento)

---

## Novidades na versão 2.2

- Planejador LLM com geração dinâmica de planos a partir do histórico e do contexto  
- Alternância em tempo real entre planners (regra ↔️ LLM) via interface no chat  
- Nova Tool: create_and_run_python_file — cria e executa scripts .py sob demanda  
- Ainda **não possui testes automatizados** — foco atual em prototipagem funcional  

---

## Arquitetura (v2.2)

![Arquitetura AI DevAgentic v2.2](architecture_v2_2.png)

---

## Legenda do Diagrama

| Ícone / Bloco             | Descrição                                                                 |
|---------------------------|---------------------------------------------------------------------------|
| 🧑 MSD                    | Pessoa desenvolvedora interagindo com o VSCode e gerando eventos          |
| 🧩 VSCode Extension       | Extensão instalada no VSCode, com WebSocket e chat webview                |
| 📁 File Watcher           | Observador de arquivos (criação, edição, remoção)                         |
| 📂 Git Watcher            | Observador de mudanças no repositório Git                                 |
| 🔌 WebSocket              | Canal bidirecional entre extensão e backend Python                        |
| 🧰 Tool Registry (extensão)| Responsável por registrar sugestões de comandos e ferramentas              |
| 🐍 Python Backend         | Núcleo inteligente executando orquestração, decisão e ferramentas         |
| 📈 Planner                | Planejador de ações com base no input do usuário                          |
| ⚙️ Decision Layer         | Componente que decide se usará ferramentas ou LLM puro                    |
| 📚 Tool Registry (backend)| Registro interno das ferramentas executáveis                              |
| 🗃️ Git Tool               | Tool concreta que executa git status, git diff, etc                        |
| 📂 File Tool              | Tool para listar, ler ou inspecionar arquivos                            |
| 🐍 Python Runner Tool     | Tool que cria e executa scripts .py sob demanda                         |

---

## Estrutura do Projeto

```
backend/
├── agent/                  # Planner, Orchestrator, FSM
├── actions/                # Implementação de ações
├── events/                 # Observadores de eventos (Git, arquivos, terminal)
├── interfaces/             # Interface LLM e OpenAI client
├── memory/                 # Memória de contexto (em desenvolvimento)
├── tools/                  # Registro e execução de ferramentas (Tool-Calling)
├── utils/                  # Utilitários diversos
├── server/                 # WebSocket API
├── main.py                 # Ponto de entrada do backend
vscode_extension/           # Extensão integrada com o VSCode (Webview + Chat)
```

---

## Requisitos

Python 3.10+  
Node.js (para extensão VSCode)  
Pacote \openai\ (Python SDK)  
Variável de ambiente \OPENAI_API_KEY\

---

## Como rodar

### Backend
```bash
uvicorn backend.main:app --reload
```

### Extensão VSCode

1. Abra a pasta \vscode_extension\ no VSCode  
2. Pressione \F5\ para iniciar a extensão em modo dev  
3. Execute o comando **Iniciar AI DevAgentic** via Command Palette

---

## Exemplos de comandos no chat

| Entrada do usuário                         | Ação executada                                 |
|--------------------------------------------|------------------------------------------------|
| qual o status do git?                      | Tool: \get_git_status()\                       |
| mostre a diferença entre os arquivos       | Tool: \get_git_diff()\                         |
| execute o comando ls                       | Tool: \run_terminal_command("ls")\             |
| liste os arquivos do projeto               | Tool: \list_project_files()\                   |
| gere e rode um script Python               | Tool: \create_and_run_python_file()\           |
| explique esse código: + código             | LLM puro (sem ferramentas)                     |

---

## Contribuindo

Crie uma issue com sugestões ou bugs  
Envie PRs com novos watchers, FSMs, planners ou tools  
Toda colaboração é bem-vinda  

---

## Licença

MIT — © 2025 AI DevAgentic
