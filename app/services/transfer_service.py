from fastapi import HTTPException

from app.core.database import supabase


def transfer_money(from_account_id: int, to_account_id: int, amount: float):
    """
    Realiza una transferencia entre dos cuentas, debitando el monto de la cuenta de origen
    y acreditándolo en la cuenta de destino. Si hay algún problema (como saldo insuficiente o
    cuentas no encontradas), se lanzan excepciones HTTP adecuadas.

    Primero, valida la existencia de ambas cuentas, luego verifica si la cuenta de origen tiene
    suficiente saldo para la transferencia. Después, realiza la transferencia actualizando los saldos
    de las cuentas y registra la transacción en la base de datos.

    Args:
    from_account_id (int): ID de la cuenta de origen desde donde se realizará la transferencia.
    to_account_id (int): ID de la cuenta de destino donde se acreditará el monto.
    amount (float): El monto a transferir.

    Returns:
    dict: Los datos de la transacción registrada.

    Raises:
    HTTPException: Si alguna cuenta no se encuentra o si no hay suficiente saldo.
    HTTPException: Si ocurre un error al registrar la transacción en la base de datos.
    """

    from_account = (
        supabase.table("accounts").select("*").eq("id", from_account_id).execute().data
    )
    to_account = (
        supabase.table("accounts").select("*").eq("id", to_account_id).execute().data
    )

    if not from_account:
        raise HTTPException(status_code=404, detail="Cuenta de origen no encontrada")

    if not to_account:
        raise HTTPException(status_code=404, detail="Cuenta de destino no encontrada")

    if from_account[0]["balance"] < amount:
        raise HTTPException(
            status_code=400, detail="Saldo insuficiente en la cuenta de origen"
        )

    supabase.table("accounts").update(
        {"balance": from_account[0]["balance"] - amount}
    ).eq("id", from_account_id).execute()

    supabase.table("accounts").update(
        {"balance": to_account[0]["balance"] + amount}
    ).eq("id", to_account_id).execute()

    transaction_data = {
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": amount,
        "status": "completada",
        "performed_at": "now()",
    }
    response = supabase.table("transactions").insert(transaction_data).execute()

    if response.data:
        return response.data[0]

    raise HTTPException(status_code=500, detail="Error al registrar la transacción")
