from app.core.database import supabase

def get_account_history(account_id):
    # Supabase query to get transaction history for the account


    print("entramos al servicio para obtener el historial")
    transactions = supabase.table("transactions").select("*").filter("from_account_id", "eq", account_id).or_("to_account_id.eq." + str(account_id)).execute()

    print("transactions", transactions)

    # Create response data
    history = []
    for transaction in transactions.data:
        # Determine direction
        direction = None
        if transaction["from_account_id"] == account_id:
            direction = "enviado"
        elif transaction["to_account_id"] == account_id:
            direction = "recibido"

        history.append({
            "transaction_id": transaction["id"],
            "transaction_type": transaction["transaction_type"],
            "amount": transaction["amount"],
            "from_account_id": transaction["from_account_id"],
            "to_account_id": transaction["to_account_id"],
            "performed_at": transaction["performed_at"],
            "direction": direction
        })

    return history
    
def get_balance(account_id):
    balance = supabase.from_("accounts").select("balance, name, id, currency, email").eq("id", account_id).execute()
    return balance
