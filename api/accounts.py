from fastapi import APIRouter, HTTPException
from app.core.database import test_connection
from app.models.account import AccountBalance, AccountCreate, AccountResponse
from app.models.transfer import TransferRequest
from app.services.account_service import get_account_balance, create_account
from app.services.transfer_service import transfer_money



# Crear el router para cuentas
router = APIRouter()

@router.get("/test-connection")
def test_db_connection():
    return test_connection()

@router.get("/account/{account_id}/balance", response_model=AccountBalance)
def get_balance(account_id: int):
    """Consulta el balance de una cuenta bancaria."""
    return get_account_balance(account_id)

@router.post("/create-account")
def create_new_account(account: AccountCreate):
    new_account = create_account(account.name, account.account_type, account.initial_balance, account.currency, account.email)
    
    if new_account:
        return {"message": "Cuenta creada con éxito", "account": new_account}
    
    raise HTTPException(status_code=500, detail="Error al crear la cuenta")

@router.post("/transfer")
def transfer(request: TransferRequest):
    """Realiza una transferencia entre cuentas"""
    try:
        transaction = transfer_money(request.from_account_id, request.to_account_id, request.amount)
        return {"status": "transferencia completada", "transaction": transaction}
    except HTTPException as e:
        raise e

