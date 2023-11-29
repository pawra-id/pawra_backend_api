from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Vet(BaseModel):
    name: str
    address: str
    clinic_name: str
    phone: str
    description: Optional[str] = ""
    image: Optional[str] = ""

class ResponseVet(Vet):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
