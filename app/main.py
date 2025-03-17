from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api import (accounts, deposit, get_balance, get_historical, transfer,
                     withdraw, ws_notifications)
from app.exceptions.account_exceptions import InvalidAccountDataError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(accounts.router, prefix="/api", tags=["accounts"])
app.include_router(transfer.router, prefix="/api", tags=["transfer"])
app.include_router(deposit.router, prefix="/api", tags=["deposit"])
app.include_router(withdraw.router, prefix="/api", tags=["withdrawal"])
app.include_router(get_balance.router, prefix="/api", tags=["get-balance"])
app.include_router(ws_notifications.router, prefix="/api", tags=["websocket"])
app.include_router(get_historical.router, prefix="/api", tags=["get-history"])


app.exception_handler(InvalidAccountDataError)


async def invalid_account_data_error_handler(request, exc: InvalidAccountDataError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.get("/")
def root():
    return {"message": "Bienvenido a la API Bancaria con FastAPI y Supabase"}
