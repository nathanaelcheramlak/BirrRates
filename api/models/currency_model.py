from pydantic import BaseModel, Field
from datetime import datetime
import uuid

class Currency(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    currency_code: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)