from pydantic import BaseModel
from datetime import datetime

class Vet(BaseModel):
    name: str
    address: str
    clinic_name: str
    phone: str
    description: str = None

class ResponseVet(Vet):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
