from fastapi import APIRouter, HTTPException
from config.database import mongodb
from schemas.currency_schema import ResponseCurrency

currency_router = APIRouter(prefix="/currency")

# GET Currencies
@currency_router.get("/")
def get_currencies() -> list[ResponseCurrency]:
    col = mongodb.get_collection("currencies")
    docs = col.find({})

    currencies = []
    for doc in docs:
        currencies.append({
            "currency_code": doc["currency_code"],
            "name": doc["name"],
        })
    return currencies

# GET Currency by Code
@currency_router.get("/{currency_code}")
def get_currency(currency_code: str) -> ResponseCurrency:
    col = mongodb.get_collection("currencies")
    doc = col.find_one({"currency_code": currency_code.upper()})
    if doc is None:
        raise HTTPException(status_code=404, detail="Currency not found")
    
    return {
        "currency_code": doc["currency_code"],
        "name": doc["name"],
    }