from pydantic import BaseModel, EmailStr,Field

class AccountBalance(BaseModel):
    account_id: int
    balance: float

class AccountCreate(BaseModel):
    name: str = Field(..., example="Juan Pérez")
    account_type: str = Field(..., example="ahorro")
    initial_balance: float = Field(..., ge=0, example=1000.50)
    currency: str = Field(..., example="MXN")
    email: EmailStr

class AccountResponse(AccountCreate):
    id: int
    created_at: str