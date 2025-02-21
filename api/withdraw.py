from fastapi import APIRouter, HTTPException
from app.models.withdraw import WithdrawalModel
from app.services.withdrawal_service import make_withdrawal

router = APIRouter()

@router.post("/withdrawal")
async def create_withdrawal(withdrawal: WithdrawalModel):
    try:
        response = make_withdrawal(withdrawal)
        return response
    except HTTPException as e:
        raise e
