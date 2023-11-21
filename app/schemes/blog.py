from pydantic import BaseModel
from datetime import datetime
from app.schemes.user import ResponseUser
from typing import Optional

class Blog(BaseModel):
    title: str
    content: str
    image: Optional[str] = None

class ResponseBlog(Blog):
    id: int
    created_at: datetime
    author: ResponseUser

    class Config:
        from_attributes = True