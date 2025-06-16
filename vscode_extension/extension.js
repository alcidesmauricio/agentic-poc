const vscode = require('vscode');
const WebSocket = require('ws');
const path = require('path');
const fs = require('fs');

let ws;

function activate(context) {
    console.log('✅ STK AI DevAgentic ativado!');

    let disposable = vscode.commands.registerCommand('stk-ai-devagentic.start', function () {
        connectWebSocket();
        showChatWebview(context);
    });

    context.subscriptions.push(disposable);
}

function connectWebSocket() {
    ws = new WebSocket('ws://localhost:8000/chat');

    ws.on('open', function () {
        console.log('🟢 WebSocket conectado ao backend!');
    });

    ws.on('message', function (message) {
        vscode.window.showInformationMessage(Resposta da AI: ${message});
    });

    ws.on('close', function () {
        console.log('🔴 WebSocket desconectado.');
    });
}

function showChatWebview(context) {
    const panel = vscode.window.createWebviewPanel(
        'stkAiDevAgenticChat',
        'STK AI DevAgentic Chat',
        vscode.ViewColumn.One,
        { enableScripts: true }
    );

    const htmlPath = path.join(context.extensionPath, 'webview', 'chat_webview.html');
    const htmlContent = fs.readFileSync(htmlPath, 'utf8');

    panel.webview.html = htmlContent;

    panel.webview.onDidReceiveMessage(
        message => {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(message.text);
            }
        },
        undefined,
        context.subscriptions
    );
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
