from pydantic import BaseModel
from datetime import datetime
from typing import List
from app.schemes.dog import ResponseDog
from app.schemes.tag import ResponseTag, Tag

class Activity(BaseModel):
    description: str

class CreateActivity(Activity):
    dog_id: int
    tags: List[Tag]

class ResponseActivity(Activity):
    id: int
    created_at: datetime
    dog: ResponseDog
    tags: List[ResponseTag]

    class Config:
        from_attributes = True
