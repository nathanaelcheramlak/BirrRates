from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.database import mongodb

from routers.bank import bank_router
from routers.currency import currency_router
from routers.exchange_rates import rate_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect()
    yield   # Application runs here
    mongodb.close()

app = FastAPI(lifespan=lifespan)

app.include_router(bank_router, prefix="/api/v1")
app.include_router(currency_router, prefix="/api/v1")
app.include_router(rate_router, prefix="/api/v1")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}