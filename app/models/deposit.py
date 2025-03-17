from typing import Optional

from pydantic import BaseModel


class MakeDepositModel(BaseModel):
    account_id: int
    amount: float
    currency: str
    transaction_type: str
