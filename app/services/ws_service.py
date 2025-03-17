import json

from app.api.ws_notifications import active_connections


async def send_deposit_notification(
    transaction_id: str, account_id: int, amount: float, currency: str, timestamp: str
):
    """
    Envía una notificación de depósito a todos los clientes WebSocket conectados.

    Esta función toma los detalles de una transacción de depósito y genera una notificación que
    se envía a todas las conexiones WebSocket activas, informando al usuario sobre el depósito.

    Args:
    transaction_id (str): El identificador único de la transacción de depósito.
    account_id (int): El ID de la cuenta que ha recibido el depósito.
    amount (float): El monto del depósito.
    currency (str): La moneda del depósito.
    timestamp (str): La fecha y hora en que se realizó la transacción.

    Returns:
    None: La función envía la notificación a las conexiones activas, pero no devuelve nada.
    """
    notification = {
        "transaction_id": transaction_id,
        "account_id": account_id,
        "amount": amount,
        "currency": currency,
        "timestamp": timestamp,
        "transaction_type": "deposit",
        "message": "Has recibido un nuevo depósito",
    }

    for connection in active_connections:
        await connection.send_text(json.dumps(notification))
