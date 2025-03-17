from pydantic import BaseModel, EmailStr, Field


class AccountBalance(BaseModel):
    account_id: int
    balance: float


class AccountCreate(BaseModel):
    name: str
    account_type: str
    initial_balance: float
    currency: str
    email: EmailStr


class AccountResponse(AccountCreate):
    id: int
    created_at: str


class AccountHistoryRequest(BaseModel):
    account_id: int
