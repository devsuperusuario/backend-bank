from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float


class TransactionCreate(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float
