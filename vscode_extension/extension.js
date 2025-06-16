const vscode = require('vscode');
const WebSocket = require('ws');

let ws;

function activate(context) {
  const disposable = vscode.commands.registerCommand('stk.startAgent', function () {
    vscode.window.showInformationMessage('🤖 stk AI DevAgentic iniciado!');

    ws = new WebSocket('ws://localhost:8000/ws');

    ws.onopen = () => {
      vscode.window.showInformationMessage('🧠 Conectado ao agente!');
    };

    ws.onmessage = (event) => {
      vscode.window.showInformationMessage('🗨️ Resposta do agente: ' + event.data);
    };

    ws.onerror = (error) => {
      vscode.window.showErrorMessage('❌ Erro no agente: ' + error.message);
    };

    // Enviar comando exemplo
    vscode.window.showInputBox({ prompt: 'Digite um comando para o agente' }).then((input) => {
      if (input && ws.readyState === WebSocket.OPEN) {
        ws.send(input);
      }
    });
  });

  context.subscriptions.push(disposable);
}

function deactivate() {
  if (ws) {
    ws.close();
  }
}

module.exports = {
  activate,
  deactivate
};
