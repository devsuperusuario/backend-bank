from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.get_balance_service import get_account_history, get_balance

# Definimos el modelo que va a recibir el body de la solicitud
class AccountHistoryRequest(BaseModel):
    account_id: int

router = APIRouter()

@router.get("/get-balance/{request}")
async def get_history(request):

    balance = get_balance(request)
    print("cuenta consultada", request)
    print(balance.data[0])
    


    # print("el id que se va a consultar es", request.account_id )
    # try:
    #     # Llama al servicio para obtener el historial de transacciones usando el account_id del cuerpo
    #     history = await get_account_history(request.account_id)
        
    #     if not history:
    #         raise HTTPException(status_code=404, detail="No se encontraron transacciones para esta cuenta.")
        
    #     return {"account_id": request.account_id, "history": history}
    
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

    return balance.data[0]
