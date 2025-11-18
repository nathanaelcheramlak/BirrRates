from fastapi import APIRouter, HTTPException
from config.database import mongodb
from schemas.bank_schema import BankResponse

bank_router =  APIRouter(prefix="/banks")

@bank_router.get("/")
def get_available_banks() -> list[BankResponse]:
    col = mongodb.get_collection("banks")
    docs = list(col.find({}))

    banks = []
    for doc in docs:
        banks.append({
            "name": doc["name"],
            "bank_code": doc["bank_code"],
        })

    return banks

@bank_router.get("/{bank_code}", response_model=BankResponse)
def get_bank(bank_code: str) -> BankResponse:
    col = mongodb.get_collection("banks")
    doc = col.find_one({"bank_code": bank_code.upper()})
    if not doc:
        raise HTTPException(status_code=404, detail="Bank not found")

    return BankResponse(
        name=doc["name"],
        bank_code=doc["bank_code"],
    )
