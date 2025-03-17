from fastapi import HTTPException, status

from app.core.database import supabase
from app.models.withdraw import WithdrawalModel


async def make_withdrawal(withdrawal: WithdrawalModel):
    """
    Realiza un retiro de dinero de una cuenta. Verifica que la cuenta exista y que tenga saldo suficiente
    antes de procesar la transacción y actualizar el saldo de la cuenta. La transacción se registra en la
    tabla de transacciones.

    Args:
    withdrawal (WithdrawalModel): Objeto que contiene la información de la transacción de retiro.

    Returns:
    dict: Mensaje de éxito y el nuevo saldo de la cuenta después del retiro.

    Raises:
    HTTPException: Si la cuenta no existe, o si el saldo es insuficiente para el retiro.
    """

    account_data = (
        supabase.table("accounts")
        .select("id, balance")
        .eq("id", withdrawal.account_id)
        .execute()
    )

    if not account_data.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Account not found"
        )

    account_balance = account_data.data[0]["balance"]

    if account_balance < withdrawal.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta cuenta no tiene los fondos suficientes para realizar el retiro",
        )

    transaction_data = {
        "to_account_id": None,
        "from_account_id": withdrawal.account_id,
        "amount": withdrawal.amount,
    }

    new_balance = account_balance - withdrawal.amount

    account_data = {"balance": new_balance}

    transaction_registry = (
        supabase.table("transactions").insert(transaction_data).execute()
    )

    balance_update = (
        supabase.table("accounts")
        .update({"balance": new_balance})
        .eq("id", withdrawal.account_id)
        .execute()
    )

    return {"message": "Withdrawal processed successfully", "new_balance": new_balance}
