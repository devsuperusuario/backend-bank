from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.get_balance_service import get_balance


class AccountHistoryRequest(BaseModel):
    """
    Modelo de solicitud para obtener el historial de la cuenta.

    Attributes:
        account_id (int): ID de la cuenta de la cual se desea obtener el balance.
    """

    account_id: int


router = APIRouter()


@router.get("/get-balance/{account_id}")
async def get_history(account_id: int):
    """
    Endpoint para obtener el balance de una cuenta específica.

    Este endpoint permite consultar el balance de una cuenta, identificada
    por su ID. Si la cuenta no existe, se retorna un error 404. Si el ID
    de la cuenta es inválido o se presenta algún error, se retornan los
    correspondientes errores 400 o 500, respectivamente.

    Args:
        account_id (int): El ID de la cuenta para la cual se consulta el balance.

    Returns:
        dict: Un diccionario con el código de estado HTTP y el balance de la cuenta.
              Si no se encuentra la cuenta, se devuelve un error 404.
              En caso de error interno, se devuelve un error 500.

    Raises:
        HTTPException: Lanza excepciones HTTP con códigos de estado adecuados:
            - 404 si no se encuentra la cuenta.
            - 400 si el ID de la cuenta es inválido.
            - 500 si ocurre un error interno del servidor.
    """
    try:
        balance = get_balance(account_id)

        if not balance:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        return {
            "status_code": 200,
            "balance": balance.data[0],
        }

    except ValueError:
        raise HTTPException(status_code=400, detail="ID de cuenta inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
