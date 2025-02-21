from fastapi import APIRouter, HTTPException
from app.models.deposit import MakeDepositModel
from app.services.deposit_service import make_deposit

# Crear el router para los depósitos
router = APIRouter()


# @router.post("/deposit")
# def deposit(deposit: MakeDepositModel):
#     """Realiza un depósito en una cuenta."""
#     try:
#         transaction = make_deposit(deposit)
#         if transaction:
#             return {"message": "Depósito exitoso", "data": transaction}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail="Error interno del servidor")

router = APIRouter()

@router.post("/deposit")
async def deposit(deposit: MakeDepositModel):
    """Realiza un depósito en una cuenta."""
    try:
        transaction = await make_deposit(deposit)  # Usa await aquí
        if transaction:
            return {"message": "Depósito exitoso", "data": transaction}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")