from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json

from backend.agent.orchestrator import Orchestrator
from backend.tools.registry import register_built_in_tools

register_built_in_tools()

app = FastAPI()
orchestrator = Orchestrator(mode="rule")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("✅ AI DevAgentic conectado com sucesso")

    while True:
        try:
            raw = await websocket.receive_text()
            print("mensagem recebida:", raw)
            data = json.loads(raw)
        except json.JSONDecodeError:
            await websocket.send_text("❌ Erro: entrada inválida.")
            continue

        # Se o tipo for mensagem do usuário
        if data.get("type") == "message":
            user_input = data.get("text", "")
            planner_mode = data.get("planner", "rule")  # padrão: rule
            orchestrator.mode = planner_mode

            print(f"[🔍] Modo atual do planner: {orchestrator.mode}")  # DEBUG opcional

            for message in orchestrator.run(user_input):
                await websocket.send_text(message)

        # Se o tipo for troca de planner (opcional)
        elif data.get("type") == "setPlanner":
            orchestrator.mode = data.get("mode", "rule")
            await websocket.send_text(f"🔧 Planner alterado para: {orchestrator.mode}")

        else:
            await websocket.send_text("❌ Erro: tipo de mensagem não reconhecido.")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)