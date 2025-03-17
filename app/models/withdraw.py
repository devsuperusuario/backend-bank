from typing import Optional

from pydantic import BaseModel


class WithdrawalModel(BaseModel):
    account_id: int
    amount: float
    performed_at: Optional[str] = None
