from pydantic import BaseModel
from typing import Optional
from app.schemes.user import User

class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: str
    user: User