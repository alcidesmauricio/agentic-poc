const vscode = require("vscode");
const path = require("path");
const fs = require("fs");
const WebSocket = require("ws");

class ChatProvider {
  constructor(context) {
    this.context = context;
    this.ws = null;
  }

  resolveWebviewView(webviewView) {
    webviewView.webview.options = { enableScripts: true };

    const htmlPath = path.join(this.context.extensionPath, "chat", "chat_webview.html");
    const html = fs.readFileSync(htmlPath, "utf-8");
    webviewView.webview.html = html;

    this.ws = new WebSocket("ws://localhost:8000/ws");

    this.ws.onopen = () => {
      console.log("✅ WebSocket conectado ao backend!");
      webviewView.webview.postMessage({
        from: "agent",
        text: "[🤖 AI DevAgentic conectado ✅]",
      });
    };

    this.ws.onmessage = (event) => {
      webviewView.webview.postMessage({
        from: "agent",
        text: event.data,
      });
    };

    this.ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      webviewView.webview.postMessage({
        from: "agent",
        text: "❌ Erro ao conectar com o backend",
      });
    };

    // recebe do chat
    webviewView.webview.onDidReceiveMessage((message) => {
      const userText = message.text;
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send(userText);
      } else {
        webviewView.webview.postMessage({
          from: "agent",
          text: "⚠️ WebSocket não está conectado.",
        });
      }
    });
  }
}

function activate(context) {
  vscode.window.showInformationMessage("✅ AI DevAgentic ativado!");
  const provider = new ChatProvider(context);
  context.subscriptions.push(
    vscode.window.registerWebviewViewProvider("aiDevAgenticView", provider)
  );
}

function deactivate() {
  console.log("Desativando DevAgentic...");
}

module.exports = { activate, deactivate };