// const vscode = require("vscode");
// const path = require("path");
// const fs = require("fs");
// const { spawn } = require("child_process");

// class ChatProvider {
//   constructor(context) {
//     this.context = context;
//     this.proc = null;
//     this.pending = new Map();
//     this.requestId = 1;
//     this.mcpReady = false;
//   }

//   resolveWebviewView(webviewView) {
//     webviewView.webview.options = { enableScripts: true };
//     const htmlPath = path.join(this.context.extensionPath, "chat", "chat_webview.html");
//     webviewView.webview.html = fs.readFileSync(htmlPath, "utf-8");

//     const serverPath = "/Users/alcides.filho/AI/agentic-poc/mcp/server2/server.py";
//     const cwd = path.dirname(serverPath);

//     // Comando completo para rodar MCP via venv
//     // Note: spawn do Windows e macOS/Linux são ligeiramente diferentes; aqui assumimos macOS/Linux
//     const shellCmd = `
//       python3 -m venv env &&
//       source env/bin/activate &&
//       pip install "mcp[cli]" &&
//       mcp dev ${serverPath}
//     `;

//     this.proc = spawn(shellCmd, {
//       cwd,
//       shell: true,
//       env: process.env,
//       stdio: ['pipe', 'pipe', 'pipe'] // stdin/stdout/stderr
//     });

//     this.proc.stdin.on('error', err => console.error('stdin error:', err));

//     this.proc.stdout.on("data", (data) => {
//       const text = data.toString();
//       console.log("MCP raw stdout:", text);

//       const lines = text.trim().split("\n");
//       for (const line of lines) {
//         // marca ready quando detecta MCP Inspector
//         if (line.includes("MCP Inspector is up")) {
//           console.log("MCP session inicializada (Inspector rodando)");
//           this.mcpReady = true;
//         } else {
//           console.log("MCP output não-JSON:", line);
//         }
//       }
//     });

//     this.proc.stderr.on("data", (data) => {
//       console.error("MCP stderr:", data.toString());
//     });

//     this.proc.on("exit", (code) => {
//       console.error(" MCP server saiu com código", code);
//       webviewView.webview.postMessage({
//         from: "agent",
//         text: `[MCP server finalizado com código ${code}]`
//       });
//     });

//     webviewView.webview.postMessage({
//       from: "agent",
//       text: "[MCP dev server iniciado via stdio]"
//     });

//     // Recebe mensagens do WebView
//     webviewView.webview.onDidReceiveMessage(async (message) => {
//       if (message.type === "call_mcp_tool") {
//         console.log("💬 Chamando git.status...");
//         const result = await this.callGitStatus();
//         console.log("💬 Resultado:", result);
//         webviewView.webview.postMessage({
//           from: "agent",
//           text: JSON.stringify(result, null, 2)
//         });
//       }
//     });
//   }

//   async callGitStatus() {
//     // aguarda MCP estar pronto
//     while (!this.mcpReady) {
//       console.log("⏳ aguardando MCP ready...");
//       await new Promise(res => setTimeout(res, 200));
//     }

//     return new Promise((resolve, reject) => {
//       const id = this.requestId++;
//       const payload = {
//         jsonrpc: "2.0",
//         id,
//         method: "tools/call",
//         params: {
//           name: "git.status",
//           arguments: { repo_path: "/Users/alcides.filho/AI/agentic-poc" },
//           _meta: { progressToken: id }
//         }
//       };

//       this.pending.set(id, { resolve, reject });
//       const jsonLine = JSON.stringify(payload) + "\n";
//       console.log("✉️ Enviando payload ao MCP:", jsonLine);

//       const ok = this.proc.stdin.write(jsonLine);
//       if (!ok) {
//         console.warn("MCP stdin buffer cheio, esperando drain");
//         this.proc.stdin.once("drain", () => console.log("MCP stdin esvaziado"));
//       }
//     });
//   }
// }

// function activate(context) {
//   const provider = new ChatProvider(context);
//   context.subscriptions.push(
//     vscode.window.registerWebviewViewProvider("aiDevAgenticView", provider)
//   );
// }

// function deactivate() {}

// module.exports = { activate, deactivate };
