from pydantic import BaseModel
from datetime import datetime
from app.schemes.user import ResponseUser
from typing import Optional

class Dog(BaseModel):
    name: str
    gender: str
    age: int
    breed: str
    neutered: Optional[bool] = False
    color: Optional[str] = None
    weight: Optional[int] = None
    height: Optional[int] = None
    description: Optional[str] = None
    microchip_id: Optional[str] = None
    image: Optional[str] = None

class ResponseDog(Dog):
    id: int
    created_at: datetime
    updated_at: datetime
    owner: ResponseUser

    class Config:
        from_attributes = True

class AdminDog(Dog):
    owner_id: int

    class Config:
        from_attributes = True

class DogAnalysis(Dog):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True