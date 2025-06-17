from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.agent.orchestrator import Orchestrator
from backend.tools.registry import register_built_in_tools
from backend.tools.registry import register_built_in_tools
register_built_in_tools()
app = FastAPI()
register_built_in_tools()
orchestrator = Orchestrator()

# CORS para permitir acesso da extensão VSCode
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("[AI DevAgentic conectado ✅]")

    while True:
        data = await websocket.receive_text()
        print(f"[Usuário 🧑‍💻] {data}")
        result = orchestrator.run(data)
        await websocket.send_text(result)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
