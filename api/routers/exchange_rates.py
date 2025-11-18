from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Optional
from config.database import mongodb

rate_router = APIRouter(prefix="/rates", tags=["Exchange Rates"])


def get_today_date() -> str:
    """Return today's date as YYYY-MM-DD string"""
    return datetime.now().strftime("%Y-%m-%d")


@rate_router.get("/latest")
def get_latest_exchange_rates(
    bank_code: Optional[str] = Query(None, description="Bank code, e.g., CBE"),
    currency_code: Optional[str] = Query(None, description="Currency code, e.g., USD")
):
    """
    Get the latest exchange rates for today.
    If no bank_code is provided, defaults to 'CBE'.
    """
    coll = mongodb.get_collection("exchange_rates")
    current_date = get_today_date()

    query = {"date": current_date, "bank_code": bank_code or "CBE"}
    if currency_code:
        query["currency_code"] = currency_code

    rate = coll.find_one(query)
    if not rate:
        raise HTTPException(
            status_code=404,
            detail=f"No exchange rates found for bank '{bank_code or 'CBE'}' on {current_date}."
        )

    return rate


@rate_router.get("/")
def get_rates(
    bank: Optional[str] = Query(None, description="Bank code, e.g., CBE"),
    currency: Optional[str] = Query(None, description="Currency code, e.g., USD"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format"),
    limit: int = Query(20, ge=1, le=100, description="Maximum number of results to return")
):
    """
    Get exchange rates filtered by bank, currency, and/or date.
    At least one of 'bank' or 'currency' must be provided.
    """
    if not bank and not currency:
        raise HTTPException(
            status_code=400,
            detail="At least one of 'bank' or 'currency' must be provided."
        )

    query_date = date or get_today_date()
    coll = mongodb.get_collection("exchange_rates")

    query = {"date": query_date}
    if bank:
        query["bank_code"] = bank
    if currency:
        query["currency_code"] = currency

    rates = list(coll.find(query).limit(limit))
    if not rates:
        raise HTTPException(
            status_code=404,
            detail=f"No exchange rates found for the given query on {query_date}."
        )

    return {"count": len(rates), "rates": rates}


@rate_router.get("/compare")
def compare_exchange_rates(
    bank: str = Query(..., description="Bank code, e.g., CBE"),
    currency: str = Query(..., description="Currency code, e.g., USD"),
    date: Optional[str] = Query(None, description="Date in YYYY-MM-DD format")
):
    """
    Compare exchange rates for a given bank and currency on a specific date.
    """
    query_date = date or get_today_date()
    coll = mongodb.get_collection("exchange_rates")

    query = {"date": query_date, "bank_code": bank, "currency_code": currency}
    rates = list(coll.find(query).limit(100))  # max 100 results by default

    if not rates:
        raise HTTPException(
            status_code=404,
            detail=f"No exchange rates found for bank '{bank}' and currency '{currency}' on {query_date}."
        )

    return {"count": len(rates), "rates": rates}
