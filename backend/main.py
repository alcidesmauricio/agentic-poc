from fastapi import FastAPI
from backend.server.websocket_server import websocket_app

app = FastAPI()

# Include WebSocket routes
app.mount("/ws", websocket_app)

@app.get("/")
def root():
    return {"message": "stk AI DevAgentic Backend Running"}
