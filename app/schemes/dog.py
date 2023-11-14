from pydantic import BaseModel
from datetime import datetime
from app.schemes.user import ResponseUser

class Dog(BaseModel):
    name: str
    gender: str
    age: int
    breed: str

class ResponseDog(Dog):
    id: int
    created_at: datetime
    owner_id: int
    owner: ResponseUser

    class Config:
        from_attributes = True
