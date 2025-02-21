from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

class TransactionCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
    # status: Optional[str] = "completada"  # Por defecto, el estado es "completada"
    # status: str
    # performed_at: Optional[datetime] = None  # Puede ser None para ser asignado por el sistema
