from pydantic import BaseModel

class ResponseCurrency(BaseModel):
    code: str
    name: str