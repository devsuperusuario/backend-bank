from fastapi import APIRouter, HTTPException
from app.models.transfer import TransactionCreate  # Asegúrate de importar el modelo adecuado
from app.services.transfer_service import transfer_money  # Llamar la lógica de transferencias

router = APIRouter()

@router.post("/transfer")
async def transfer_money(transaction: TransactionCreate):
    # Llama al servicio de transferencias para procesar la transacción
    result = await transfer_money(transaction)
    if result:
        return {"message": "Transferencia completada", "data": result}
    else:
        raise HTTPException(status_code=400, detail="Error en la transferencia")
