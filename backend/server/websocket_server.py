from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
from starlette.websockets import WebSocketDisconnect
from backend.agent.orchestrator import Orchestrator
from backend.tools.registry import register_built_in_tools
from backend.tools.dynamic_agents_loader import list_all_agents, load_dynamic_agents

register_built_in_tools()

app = FastAPI()
orchestrator = Orchestrator(mode="rule")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/agents")
def list_agents():
    return list_all_agents()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("✅ AI DevAgentic conectado com sucesso")
    try:
        while True:
            try:
                raw = await websocket.receive_text()
                print("mensagem recebida:", raw)
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_text("❌ Erro: entrada inválida.")
                continue

            if data.get("type") == "message":
                user_input = data.get("text", "")
                planner_mode = data.get("planner", "rule")
                master_agent_name = data.get("master_agent")
                child_agents_names = data.get("child_agents", [])

                print(f"[🔍] Modo atual do planner: {planner_mode}")

                # Carregar agentes
                all_agents = list_all_agents()
                master_agent = next((a for a in all_agents if a["name"] == master_agent_name), None) if master_agent_name else None
                child_agents = [a for a in all_agents if a["name"] in child_agents_names] if child_agents_names else []

                orchestrator = Orchestrator(
                    mode=planner_mode,
                    master_agent=master_agent,
                    child_agents=child_agents
                )

                async for message in orchestrator.run(user_input):
                    await websocket.send_text(message)

            elif data.get("type") == "setPlanner":
                orchestrator.mode = data.get("mode", "rule")
                await websocket.send_text(f"🔧 Planner alterado para: {orchestrator.mode}")

            else:
                await websocket.send_text("❌ Erro: tipo de mensagem não reconhecido.")
    except WebSocketDisconnect:
        print("Cliente WebSocket desconectado.")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)