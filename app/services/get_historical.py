from app.core.database import supabase


def get_account_history(account_id):
    """
    Función para recuperar el historial de transacciones de una cuenta específica.
    Esta función consulta la base de datos de transacciones y filtra aquellas que
    están asociadas al 'account_id' ya sea como 'from_account_id' o 'to_account_id'.

    Args:
        account_id (int): ID de la cuenta cuyo historial de transacciones se va a recuperar.

    Returns:
        list: Lista de transacciones asociadas al account_id.
        None: Si no se encuentran transacciones para la cuenta.

    Raises:
        Exception: Si ocurre algún error durante la consulta a la base de datos.
    """

    try:
        transactions = (
            supabase.table("transactions")
            .select("*")
            .or_(f"from_account_id.eq.{account_id},to_account_id.eq.{account_id}")
            .execute()
        )

        if not transactions.data:
            return None

        return transactions.data

    except Exception as e:
        raise Exception(
            f"Error al obtener el historial de transacciones para la cuenta {account_id}: {str(e)}"
        )
