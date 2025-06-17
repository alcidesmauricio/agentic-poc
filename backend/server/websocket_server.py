from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from backend.agent.orchestrator import Orchestrator
from backend.tools.registry import register_built_in_tools

register_built_in_tools()

app = FastAPI()
orchestrator = Orchestrator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("[🤖] AI DevAgentic conectado com sucesso ✅")

    while True:
        data = await websocket.receive_text()
        for message in orchestrator.run(data):
            await websocket.send_text(message)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    



    