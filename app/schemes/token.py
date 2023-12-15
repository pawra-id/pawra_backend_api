from pydantic import BaseModel
from typing import Optional
from app.schemes.user import ResponseUser

class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: str
    user: ResponseUser

class RefreshToken(BaseModel):
    access_token: str