from app.core.database import supabase


def get_account_history(account_id):
    """
    Obtiene el historial de transacciones para una cuenta específica.

    Esta función consulta la base de datos para obtener todas las transacciones asociadas
    a una cuenta, tanto como cuenta emisora ("from_account_id") como cuenta receptora
    ("to_account_id"). Luego, clasifica cada transacción como "enviado" o "recibido"
    según corresponda, y devuelve una lista con la información detallada de las transacciones.

    Args:
    account_id (int): El ID de la cuenta para la que se desea obtener el historial de transacciones.

    Returns:
    list: Una lista de diccionarios, cada uno representando una transacción con detalles como:
          ID de transacción, tipo de transacción, monto, cuentas involucradas, fecha y dirección.
    """

    transactions = (
        supabase.table("transactions")
        .select("*")
        .filter("from_account_id", "eq", account_id)
        .or_("to_account_id.eq." + str(account_id))
        .execute()
    )

    history = []
    for transaction in transactions.data:
        direction = None
        if transaction["from_account_id"] == account_id:
            direction = "enviado"
        elif transaction["to_account_id"] == account_id:
            direction = "recibido"

        history.append(
            {
                "transaction_id": transaction["id"],
                "transaction_type": transaction["transaction_type"],
                "amount": transaction["amount"],
                "from_account_id": transaction["from_account_id"],
                "to_account_id": transaction["to_account_id"],
                "performed_at": transaction["performed_at"],
                "direction": direction,
            }
        )

    return history


def get_balance(account_id):
    """
    Obtiene el balance de una cuenta específica.

    Esta función consulta la base de datos para obtener el balance actual de una cuenta,
    junto con información adicional como el nombre de la cuenta, la moneda y el correo electrónico
    asociado. Si la cuenta no se encuentra, devuelve None.

    Args:
    account_id (int): El ID de la cuenta cuyo balance se desea obtener.

    Returns:
    dict: Un diccionario con la información de la cuenta, que incluye balance, nombre,
          moneda y correo electrónico.
    None: Si no se encuentran datos para la cuenta especificada.

    Raises:
    ValueError: Si ocurre un error durante la consulta del balance.
    """
    try:
        balance = (
            supabase.from_("accounts")
            .select("balance, name, id, currency, email")
            .eq("id", account_id)
            .execute()
        )

        if not balance.data:
            return None

        return balance
    except Exception as e:
        raise ValueError("Error al obtener el balance de la cuenta") from e
