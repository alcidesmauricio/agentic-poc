from fastapi import APIRouter, WebSocket
from backend.agentic_core.fsm.state_machine import state_machine
from backend.agentic_core.llm_clients.openai_client import OpenAIClient

websocket_app = APIRouter()

openai_client = OpenAIClient()

@websocket_app.websocket("/chat")
async def websocket_chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Passar pelo FSM antes de responder
        action = state_machine.process_event(data)
        response = openai_client.get_completion(action)
        await websocket.send_text(response)
