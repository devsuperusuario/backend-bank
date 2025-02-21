from pydantic import BaseModel
from typing import Optional

class MakeDepositModel(BaseModel):
    account_id: int
    amount: float
    currency: str
    transaction_type: str
