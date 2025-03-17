import ast

from fastapi import APIRouter, HTTPException

from app.core.database import test_connection
from app.models.account import AccountBalance, AccountCreate, AccountResponse
from app.models.transfer import TransferRequest
from app.services.account_service import create_account
from app.services.transfer_service import transfer_money

router = APIRouter()


@router.get("/test-connection")
def test_db_connection():
    """
    Endpoint para verificar la conexión a la base de datos.

    Este endpoint realiza una prueba de conexión a la base de datos
    y devuelve un mensaje que indica si la conexión fue exitosa.

    Returns:
        str: Mensaje de estado de la conexión.
    """
    return test_connection()


@router.post("/create-account")
def create_new_account(account: AccountCreate):
    """
    Crea una nueva cuenta bancaria.

    Este endpoint permite crear una cuenta bancaria proporcionando
    los datos necesarios como nombre, tipo de cuenta, saldo inicial,
    moneda y correo electrónico.

    Args:
        account (AccountCreate): Los datos necesarios para crear la cuenta.

    Returns:
        dict: Mensaje de éxito y los detalles de la cuenta creada.

    Raises:
        HTTPException: Si ocurre un error al crear la cuenta.
    """

    new_account = create_account(
        account.name,
        account.account_type,
        account.initial_balance,
        account.currency,
        account.email,
    )

    if new_account:
        return {"message": "Estado de la creación de la cuenta", "account": new_account}

    raise HTTPException(status_code=500, detail="Error al crear la cuenta")


@router.post("/transfer")
def transfer(request: TransferRequest):
    """
    Realiza una transferencia entre cuentas.

    Este endpoint permite transferir dinero de una cuenta a otra.
    Asegúrese de que ambas cuentas existen y el saldo de la cuenta
    de origen sea suficiente antes de realizar la transferencia.

    Args:
        request (TransferRequest): Los datos de la transferencia, incluyendo
                                    las cuentas de origen y destino y el monto.

    Returns:
        dict: Estado de la transferencia y detalles de la transacción.

    Raises:
        HTTPException: Si ocurre algún error durante la transferencia.
    """
    try:
        transaction = transfer_money(
            request.from_account_id, request.to_account_id, request.amount
        )
        return {"status": "transferencia completada", "transaction": transaction}
    except HTTPException as e:
        raise e
