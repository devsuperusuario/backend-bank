from fastapi import APIRouter, HTTPException

from app.models.deposit import MakeDepositModel
from app.services.deposit_service import make_deposit

router = APIRouter()


@router.post("/deposit")
async def deposit(deposit: MakeDepositModel):
    """
    Realiza un depósito en una cuenta.

    Este endpoint recibe un objeto que contiene la información del depósito,
    realiza la validación necesaria y registra el depósito en la base de datos.
    Si el depósito es exitoso, se devuelve un mensaje con los detalles de la transacción.

    Parámetros:
    - deposit (MakeDepositModel): Modelo con los detalles del depósito (como la cuenta, monto, etc.)

    Respuesta:
    - 200: Depósito exitoso con los detalles de la transacción.
    - 400: Si hay un error en los datos proporcionados (por ejemplo, monto negativo).
    - 500: Error en el servidor si ocurre un problema inesperado.
    """
    try:
        transaction = await make_deposit(deposit)
        if transaction:
            return {"message": "Depósito exitoso", "data": transaction}
    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:

        raise HTTPException(status_code=500, detail="Error interno del servidor")
