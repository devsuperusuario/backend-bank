from app.models.account import AccountBalance
from app.core.database import supabase


def get_account_balance(account_id: int) -> AccountBalance:
    """Simula obtener el balance de una cuenta"""
    # Aquí simula que consultas la base de datos
    # Por ejemplo, balance de cuenta ficticia
    simulated_balance = 9999.50  # Balance simulado para cualquier cuenta
    return AccountBalance(account_id=account_id, balance=simulated_balance)

def create_account(name: str, account_type: str, initial_balance: float, currency: str, email: str):
    """Inserta una nueva cuenta en Supabase"""
    data = {
        "name": name,
        "account_type": account_type,
        "balance": initial_balance,  # Se almacena el balance inicial en la columna "balance"
        "currency": currency,
        "email": email
    }
    
    try:
        response = supabase.table("accounts").insert(data).execute()
        
        if response.data:
            return response.data[0]  # Devolver la cuenta creada
        
        return None  # Manejo en caso de que no se cree la cuenta

    except Exception as e:
        print(f"Error al crear la cuenta: {e}")
        return None