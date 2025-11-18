from pydantic import BaseModel, Field, HttpUrl
import uuid
from datetime import datetime

class Bank(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    bank_code: str
    scrape_url: HttpUrl
    created_at: datetime = Field(default_factory=datetime.now())
    updated_at: datetime = Field(default_factory=datetime.now())