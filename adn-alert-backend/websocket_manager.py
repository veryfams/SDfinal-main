import json
from fastapi import WebSocket
from typing import Set

class WebSocketManager:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.add(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.connections.discard(websocket)

    async def broadcast(self, message: dict):
        print(f"📣 Enviando mensaje a {len(self.connections)} clientes WebSocket...")
        dead_connections = set()
        for ws in self.connections:
            try:
                await ws.send_text(json.dumps(message))
            except Exception as e:
                print("❌ Error al enviar a un cliente WS:", e)
                dead_connections.add(ws)
        for ws in dead_connections:
            self.connections.discard(ws)

