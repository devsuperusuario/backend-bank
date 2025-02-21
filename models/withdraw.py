from pydantic import BaseModel
from typing import Optional

class WithdrawalModel(BaseModel):
    account_id: int
    amount: float
    performed_at: Optional[str] = None  # Fecha de la transacción (opcional)
