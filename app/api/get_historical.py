from fastapi import APIRouter, HTTPException

from app.models.account import AccountHistoryRequest
from app.services.get_historical import get_account_history

router = APIRouter()


@router.get("/get-historical/{request}")
async def get_history(request: int):
    """
    Endpoint para obtener el historial de transacciones de una cuenta específica.

    Este endpoint consulta el historial de transacciones asociadas a una cuenta,
    identificada por su ID. Si no se encuentran datos para la cuenta, se retornará
    un error 404. Si se presenta algún otro error, se manejará mediante un
    error 500.

    Args:
        request (int): ID de la cuenta para la cual se consulta el historial de transacciones.

    Returns:
        dict: Un diccionario con el código de estado HTTP y el historial de la cuenta.

    Raises:
        HTTPException: Lanza excepciones HTTP con los siguientes códigos de estado:
            - 404 si no se encuentran transacciones para la cuenta.
            - 400 si el ID de la cuenta es inválido.
            - 500 si ocurre un error interno del servidor.
    """
    try:

        historical = get_account_history(request)

        if historical is None:
            raise HTTPException(
                status_code=404, detail="Historial no encontrado para esta cuenta"
            )

        return {
            "status_code": 200,
            "historical": historical,
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="ID de cuenta inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
