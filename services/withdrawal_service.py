from app.models.withdraw import WithdrawalModel
from app.core.database import supabase
from fastapi import HTTPException, status


def make_withdrawal(withdrawal: WithdrawalModel):
    print("ENTRAMOS A MAKE_WITHDRAWAL")
    print("los datos que llegan a make_withdraw son:", withdrawal)
    # Obtenemos la cuenta y verificamos saldo suficiente en una sola consulta
    account_data = supabase.table("accounts").select("id, balance").eq("id", withdrawal.account_id).execute()

    print("ENTRAMOS A MAKE_WITHDRAWAL2")

    if not account_data.data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )

    account_balance = account_data.data[0]["balance"]
    print("el dinero en la cuenta antes de retirar es:", account_balance)

    if account_balance < withdrawal.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )

    # Realizamos la transacción de retiro y actualizamos el saldo de forma atómica
    transaction_data = {
        "to_account_id": None,
        "from_account_id": withdrawal.account_id,
        "amount": withdrawal.amount,
        # "performed_at": withdrawal.performed_at or "CURRENT_TIMESTAMP",  # Fecha actual si no se proporciona
        "transaction_type": "retiro",
    }

    new_balance = account_balance - withdrawal.amount
    print("nuevo saldo después del retiro es:", new_balance)

    account_data= {
        # "id": withdrawal.account_id,
        "balance": new_balance

    }

    transaction_registry = supabase.table("transactions").insert(transaction_data).execute()
    # balance_update = supabase.table("accounts").update(account_data)
    balance_update = supabase.table("accounts").update({"balance": new_balance}).eq("id", withdrawal.account_id).execute()
    print("balance update", balance_update)
    # if balance_update.status_code == 200:
    #     print("Balance actualizado correctamente.")
    # else:
    #     print("Error al actualizar el balance:", balance_update.text)











    # # Insertamos la transacción y actualizamos el saldo
    # with supabase.transaction() as tx:
    #     tx.table("transactions").insert(data).execute()
    #     new_balance = account_balance - withdrawal.amount
    #     tx.table("accounts").update({"balance": new_balance}).eq("id", withdrawal.account_id).execute()




    return {"message": "Withdrawal processed successfully", "new_balance": new_balance}
    # return "ok"