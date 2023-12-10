from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = ""
    summary: Optional[str] = ""
    address: Optional[str] = ""
    image: Optional[str] = ""
    summary: Optional[str] = ""
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""
    
class CreateUser(User):
    password: str

class ResponseUser(User):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

