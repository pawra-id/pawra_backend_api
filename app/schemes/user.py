from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    summary: str = None
    address: str = None
    
class CreateUser(User):
    password: str

class ResponseUser(User):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

