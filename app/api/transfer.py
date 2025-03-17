from fastapi import APIRouter, HTTPException

from app.models.transfer import TransactionCreate
from app.services.transfer_service import transfer_money

router = APIRouter()


@router.post("/transfer")
async def transfer_money_endpoint(transaction: TransactionCreate):
    """
    Endpoint para realizar una transferencia de dinero entre cuentas.

    Este endpoint recibe los datos de una transferencia y llama al servicio de
    transferencia para procesar la transacción. Si la transferencia se realiza
    con éxito, retorna un mensaje con el detalle. Si ocurre un error, se maneja
    con un código de error adecuado.

    Args:
        transaction (TransactionCreate): Los datos de la transacción.

    Returns:
        dict: Un mensaje de éxito o error con un código de estado HTTP adecuado.

    Raises:
        HTTPException: Si ocurre un error en la transferencia, se lanzan errores HTTP
            con los códigos 400 o 500.
    """
    try:
        result = await transfer_money(transaction)

        return {"message": "Transferencia completada", "data": result}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error en la transferencia: {str(e)}"
        )
