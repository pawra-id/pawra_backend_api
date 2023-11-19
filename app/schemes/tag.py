from pydantic import BaseModel
from datetime import datetime

class Tag(BaseModel):
    name: str

class ResponseTag(Tag):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True