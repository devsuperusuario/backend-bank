# from supabase import create_client, Client
# from app.models.deposit import MakeDepositModel
# from app.core.database import supabase
# from app.services.get_balance_service import get_balance


# def make_deposit(deposit: MakeDepositModel):
#     # Verificar si la cuenta existe antes de hacer el depósito
#     account = supabase.table("accounts").select("id").eq("id", deposit.account_id).execute()
#     actual_balance = get_balance(deposit.account_id).data[0]['balance']
#     print("el balance obtenido en el servicio para depositar es:", actual_balance )

#     if not account.data:
#         raise ValueError(f"La cuenta con ID {deposit.account_id} no existe.")

#     # Si la cuenta existe, proceder con la inserción
#     data = {
#         "to_account_id": deposit.account_id,
#         "amount": deposit.amount,
#         "transaction_type" : deposit.transaction_type

#     }

#     new_balance = actual_balance + deposit.amount


#     res_transactions = supabase.table("transactions").insert(data).execute()

    

#     res_accounts = supabase.table("accounts").update({"balance": new_balance}).eq("id", deposit.account_id).execute()

#     return res_transactions


from supabase import create_client, Client
from app.models.deposit import MakeDepositModel
from app.core.database import supabase
from app.services.get_balance_service import get_balance
from app.services.ws_service import send_deposit_notification
from datetime import datetime
import asyncio

async def make_deposit(deposit: MakeDepositModel):
    """Procesa un depósito en una cuenta y envía una notificación WebSocket."""
    account = supabase.table("accounts").select("id").eq("id", deposit.account_id).execute()
    actual_balance = get_balance(deposit.account_id).data[0]['balance']

    if not account.data:
        raise ValueError(f"La cuenta con ID {deposit.account_id} no existe.")

    new_balance = actual_balance + deposit.amount
    data = {
        "to_account_id": deposit.account_id,
        "amount": deposit.amount,
        "transaction_type": deposit.transaction_type
    }

    res_transactions = supabase.table("transactions").insert(data).execute()
    res_accounts = supabase.table("accounts").update({"balance": new_balance}).eq("id", deposit.account_id).execute()

    # Obtener ID de transacción y fecha
    transaction_id = res_transactions.data[0]["id"]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    # Enviar notificación WebSocket
    asyncio.create_task(send_deposit_notification(transaction_id, deposit.account_id, deposit.amount, "MXN", timestamp))

    return res_transactions
