from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

# Lista para almacenar conexiones WebSocket activas
active_connections: List[WebSocket] = []

@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    """Maneja conexiones WebSocket para enviar notificaciones de depósitos."""
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Mantener la conexión abierta
    except WebSocketDisconnect:
        active_connections.remove(websocket)
