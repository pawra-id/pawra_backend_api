from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    username: str
    email: EmailStr
    summary: Optional[str] = ""
    address: Optional[str] = ""
    image: Optional[str] = ""
    summary: Optional[str] = ""
    
class CreateUser(User):
    password: str

class ResponseUser(User):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True

