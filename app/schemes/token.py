from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str