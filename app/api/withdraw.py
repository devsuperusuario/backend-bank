from fastapi import APIRouter, HTTPException, status

from app.models.withdraw import WithdrawalModel
from app.services.withdrawal_service import make_withdrawal

router = APIRouter()


@router.post("/withdrawal")
async def create_withdrawal(withdrawal: WithdrawalModel):
    """
    Endpoint para realizar un retiro de dinero desde una cuenta.

    Este endpoint recibe los detalles de un retiro y llama al servicio `make_withdrawal`
    para procesarlo. Si el retiro es exitoso, se retorna un mensaje de éxito con el código de estado 200.
    En caso de error, se maneja con un código de estado HTTP adecuado.

    Args:
        withdrawal (WithdrawalModel): Modelo con los datos del retiro.

    Returns:
        dict: Un mensaje con el detalle del retiro o un mensaje de error.

    Raises:
        HTTPException: Si ocurre un error en el servicio de retiro, se lanza un error HTTP
            con un código de estado adecuado (400 para errores de datos, 404 para recursos no encontrados,
            500 para errores internos).
    """
    try:
        response = await make_withdrawal(withdrawal)

        return {
            "message": response["message"],
            "new_balance": response["new_balance"],
            "status_code": 200,
        }

    except HTTPException as e:

        return e

    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=str(ve),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}",
        )
