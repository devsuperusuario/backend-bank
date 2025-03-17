import asyncio
from datetime import datetime

from app.core.database import supabase
from app.models.deposit import MakeDepositModel
from app.services.get_balance_service import get_balance
from app.services.ws_service import send_deposit_notification


async def make_deposit(deposit: MakeDepositModel):
    """
    Procesa un depósito en una cuenta y envía una notificación WebSocket.

    Esta función recibe un objeto de tipo MakeDepositModel que contiene los datos del
    depósito, como el ID de la cuenta, el monto a depositar y el tipo de transacción.
    Luego, consulta la cuenta en la base de datos, actualiza el balance y registra la
    transacción en la tabla correspondiente. Finalmente, envía una notificación WebSocket
    a los usuarios conectados para informarles del depósito realizado.

    Args:
    deposit (MakeDepositModel): El objeto que contiene los datos del depósito, como
                                 el ID de la cuenta, monto, y tipo de transacción.

    Returns:
    dict: Un diccionario con la respuesta de la inserción de la transacción en la base
          de datos, que contiene detalles de la transacción procesada.

    Raises:
    ValueError: Si la cuenta asociada al depósito no existe.
    """
    account = (
        supabase.table("accounts").select("id").eq("id", deposit.account_id).execute()
    )

    actual_balance = get_balance(deposit.account_id).data[0]["balance"]

    if not account.data:
        raise ValueError(f"La cuenta con ID {deposit.account_id} no existe.")

    new_balance = actual_balance + deposit.amount

    data = {
        "to_account_id": deposit.account_id,
        "amount": deposit.amount,
        "transaction_type": deposit.transaction_type,
    }

    res_transactions = supabase.table("transactions").insert(data).execute()

    res_accounts = (
        supabase.table("accounts")
        .update({"balance": new_balance})
        .eq("id", deposit.account_id)
        .execute()
    )

    transaction_id = res_transactions.data[0]["id"]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    asyncio.create_task(
        send_deposit_notification(
            transaction_id, deposit.account_id, deposit.amount, "MXN", timestamp
        )
    )

    return res_transactions
