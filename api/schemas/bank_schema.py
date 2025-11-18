from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional

class CreateBank(BaseModel):
    name: str
    bank_code: str
    scrape_url: HttpUrl

class UpdateBank(BaseModel):
    name: Optional[str] = None
    bank_code: Optional[str] = None
    scrape_url: Optional[HttpUrl] = None

class BankResponse(BaseModel):
    name: str
    bank_code: str

