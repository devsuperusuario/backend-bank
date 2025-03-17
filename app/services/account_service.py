from app.core.database import supabase
from app.exceptions.account_exceptions import (AccountCreationError,
                                               InvalidAccountDataError)
from app.utils.email_duplicate_validator import email_duplicate_validator


def create_account(
    name: str, account_type: str, initial_balance: float, currency: str, email: str
):
    """
    Función para crear una cuenta, validando los datos de la cuenta.

    Args:
    name (str): Nombre del titular de la cuenta.
    account_type (str): Tipo de cuenta (ahorro, corriente, etc).
    initial_balance (float): Saldo inicial de la cuenta.
    currency (str): Moneda en que se abrirá la cuenta (por ejemplo, "MXN").
    email (str): Correo electrónico asociado a la cuenta.

    Returns:
    dict: Datos de la cuenta creada o None si hubo un error.
    """
    if initial_balance < 0:
        raise InvalidAccountDataError("El saldo inicial no puede ser negativo.")

    data = {
        "name": name,
        "account_type": account_type,
        "balance": initial_balance,
        "currency": currency,
        "email": email,
    }

    try:
        response = supabase.table("accounts").insert(data).execute()

        if response.data:
            return response.data
        else:
            raise AccountCreationError(
                "No se pudo crear la cuenta, no se recibieron datos válidos."
            )

    except Exception as e:
        raise AccountCreationError(f"Error inesperado al crear la cuenta: {str(e)}")
