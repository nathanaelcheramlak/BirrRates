from pydantic import BaseModel, Field
from datetime import date, datetime, timezone
import uuid

class ExchangeRate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    bank_code: str     # maps to Bank.bank_code
    currency_code: str # maps to Currency.code
    
    cash_buying_rate: float
    cash_selling_rate: float
    transaction_buying_rate: float
    transaction_selling_rate: float

    # yyyy-mm-dd
    rate_date: date 
    
    # Timestamp
    scrape_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))