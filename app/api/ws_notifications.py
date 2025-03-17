from typing import List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

active_connections: List[WebSocket] = []


@router.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    """
    Esta función maneja las conexiones WebSocket entrantes para enviar notificaciones
    a los clientes. El endpoint es utilizado por los clientes para recibir notificaciones
    de eventos en tiempo real, como depósitos. La función gestiona el ciclo de vida
    de la conexión WebSocket.

    1. Se acepta la conexión WebSocket entrante para permitir la comunicación bidireccional
       con el cliente.
    2. La conexión WebSocket se agrega a la lista de conexiones activas para mantener
       un registro de todos los clientes conectados.
    3. La función entra en un bucle infinito esperando recibir datos del cliente.
    4. Si el cliente se desconecta, la conexión se elimina de la lista de conexiones activas.

    Args:
        websocket (WebSocket): El objeto WebSocket que representa la conexión con el cliente.
    """
    await websocket.accept()

    active_connections.append(websocket)

    try:

        while True:

            await websocket.receive_text()
    except WebSocketDisconnect:

        active_connections.remove(websocket)
