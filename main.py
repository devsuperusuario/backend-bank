from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import accounts, transfer, deposit, withdraw, get_balance, ws_notifications

app = FastAPI()

# Habilitar CORS para que el frontend pueda hacer peticiones (opcional pero recomendado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto si solo quieres permitir ciertos dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def read_root():
#     return {"Hello World en la raíz del proyecto"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}


# Registrar los routers
app.include_router(accounts.router, prefix="/api", tags=["accounts"])
app.include_router(transfer.router, prefix="/api", tags=["transfer"]) 
app.include_router(deposit.router, prefix="/api", tags=["deposit"])
app.include_router(withdraw.router, prefix="/api", tags=["withdrawal"])
app.include_router(get_balance.router, prefix="/api", tags=["get-balance"])
app.include_router(ws_notifications.router, prefix="/api", tags=["websocket"])


@app.get("/")
def root():
    return {"message": "Bienvenido a la API Bancaria con FastAPI y Supabase"}