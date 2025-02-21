from app.core.database import supabase
from fastapi import HTTPException

def transfer_money(from_account_id: int, to_account_id: int, amount: float):
    """Realiza una transferencia entre dos cuentas"""

    
    # Verificar si las cuentas existen
    from_account = supabase.table("accounts").select("*").eq("id", from_account_id).execute().data
    to_account = supabase.table("accounts").select("*").eq("id", to_account_id).execute().data
    
    if not from_account:
        raise HTTPException(status_code=404, detail="Cuenta de origen no encontrada")
    
    if not to_account:
        raise HTTPException(status_code=404, detail="Cuenta de destino no encontrada")
    
    # Verificar saldo en la cuenta de origen
    if from_account[0]["balance"] < amount:
        raise HTTPException(status_code=400, detail="Saldo insuficiente en la cuenta de origen")
    
    # Realizar la transferencia: debitar de la cuenta de origen y acreditar en la cuenta de destino
    # Actualizar saldo de la cuenta de origen
    supabase.table("accounts").update({"balance": from_account[0]["balance"] - amount}).eq("id", from_account_id).execute()

    # Actualizar saldo de la cuenta de destino
    supabase.table("accounts").update({"balance": to_account[0]["balance"] + amount}).eq("id", to_account_id).execute()
    
    # Registrar la transacción en la tabla de transacciones
    transaction_data = {
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": amount,
        "status": "completada",  # El estado es "completada" por defecto
        "performed_at": "now()"
    }
    response = supabase.table("transactions").insert(transaction_data).execute()
    
    if response.data:
        return response.data[0]  # Devolver la transacción creada
    raise HTTPException(status_code=500, detail="Error al registrar la transacción")
