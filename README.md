# 📦 STK AI DevAgentic - v2.0 (MVP Consolidado)

> **Agentic AI para desenvolvedores no VSCode com backend Python + frontend VSCode Extension.**

---

## 📌 Visão Geral

O **STK AI DevAgentic** é um agente de software agentic, que atua como um copiloto de desenvolvimento **dentro do VSCode**, com foco em **assistência proativa**, **interpretação de linguagem natural**, **integração com o terminal**, **Git awareness**, **file awareness** e **integração com OpenAI para LLMs**.

---

## 🚀 Principais Features da v2.0

| Feature                                 | Status      |
|---------------------------------------- | ----------- |
| Arquitetura Agentic FSM (Finite State Machine) | ✅ |
| Chat com streaming via WebSocket          | ✅ |
| Monitoramento de Terminal (Várias Instâncias) | ✅ |
| Monitoramento de Arquivos (file watcher) | ✅ |
| Monitoramento de Git (commit, push, pull) | ✅ |
| Camada de decisão Agentic com automação | ✅ |
| Ações automáticas sobre terminal, git e arquivos | ✅ |
| Extensão para VSCode com Webview | ✅ |
| Suporte a interação via linguagem natural | ✅ |
| Sugestão de comandos de terminal | ✅ |
| Execução de comandos de terminal via chat | ✅ |

---

## 📡 Diagrama Mermaid (Arquitetura da Solução)

\\\`mermaid
graph TD
    Client(👨‍💻 VSCode Client)
    ChatWebview[💬 Chat Webview]
    TerminalListener[🖥️ Terminal Event Listener]
    FileWatcher[📂 File Watcher]
    GitWatcher[🔀 Git Watcher]

    Backend(🧠 Python Backend - FastAPI + FSM + Decision Layer)
    WebSocketServer[🔌 WebSocket Server]
    OpenAIClient[🤖 OpenAI LLM Client]
    FSM[🔁 FSM - Finite State Machine]
    DecisionLayer[🧭 Decision Layer]
    ContextManager[📋 Context Manager]
    TerminalManager[🖥️ Terminal Manager]
    GitManager[📂 Git Manager]
    FileActions[🗃️ File Actions]
    TerminalActions[🖥️ Terminal Actions]
    GitActions[🔀 Git Actions]

    Client -->|User inputs| ChatWebview
    ChatWebview -->|WebSocket| WebSocketServer
    TerminalListener -->|Events| WebSocketServer
    FileWatcher -->|Events| WebSocketServer
    GitWatcher -->|Events| WebSocketServer

    WebSocketServer --> Backend
    Backend --> FSM
    Backend --> DecisionLayer
    Backend --> OpenAIClient
    Backend --> ContextManager
    DecisionLayer --> TerminalActions
    DecisionLayer --> FileActions
    DecisionLayer --> GitActions
\\\`

---

## 🧱 Estrutura de Pastas da v2.0

\\\`
stk_ai_devagentic/
├── backend/
│   ├── agentic_core/
│   │   ├── actions/
│   │   ├── decision/
│   │   ├── event_listeners/
│   │   ├── fsm/
│   │   └── llm_clients/
│   ├── server/
│   └── utils/
├── vscode_extension/
│   ├── chat/
│   ├── events/
│   ├── terminal/
│   └── webview/
└── tests/
\\\`

---

## ✅ Explicação de Cada Bloco do Diagrama

| Componente | Função |
|---|---|
| **👨‍💻 VSCode Client** | Onde o desenvolvedor interage. |
| **💬 Chat Webview** | UI de chat, envia e recebe mensagens via WebSocket. |
| **🖥️ Terminal Event Listener** | Captura tudo o que o usuário digita e a saída dos terminais no VSCode. |
| **📂 File Watcher** | Detecta alterações em arquivos do workspace. |
| **🔀 Git Watcher** | Detecta ações Git locais (commit, pull, push, etc.). |
| **🔌 WebSocket Server** | Ponte de comunicação bidirecional entre VSCode Extension e Backend Python. |
| **🧠 Backend Python** | Onde mora a inteligência agentic. |
| **🔁 FSM** | Máquina de estados que controla os fluxos agentic. |
| **🧭 Decision Layer** | Camada de decisão: decide quando agir automaticamente. |
| **🤖 OpenAI LLM Client** | Faz chamadas OpenAI (chat completions, etc). |
| **📋 Context Manager** | Mantém o estado e contexto atual do projeto. |
| **🖥️ Terminal Manager** | Permite executar comandos diretamente no terminal via backend. |
| **📂 Git Manager** | Faz interação programática com Git. |
| **🗃️ File Actions** | Lê, edita ou cria arquivos automaticamente. |
| **🖥️ Terminal Actions** | Permite o backend disparar comandos no terminal. |
| **🔀 Git Actions** | Executa comandos Git de forma programada. |

---

## 📚 Próximos Passos (Para v2.x e além)

Logging detalhado
Testes unitários
Suporte multi-LLM
Interface gráfica interativa para contexto de projeto
Modo copiloto automático (proatividade total)

