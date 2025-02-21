import json
from app.api.ws_notifications import active_connections

async def send_deposit_notification(transaction_id: str, account_id: int, amount: float, currency: str, timestamp: str):
    """Envía una notificación de depósito a todos los clientes WebSocket conectados."""
    notification = {
        "transaction_id": transaction_id,
        "account_id": account_id,
        "amount": amount,
        "currency": currency,
        "timestamp": timestamp,
        "transaction_type": "deposit",
        "message": "Has recibido un nuevo depósito"
    }
    
    # Enviar la notificación a todas las conexiones activas
    for connection in active_connections:
        await connection.send_text(json.dumps(notification))
