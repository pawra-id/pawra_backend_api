from pydantic import BaseModel
from datetime import datetime
from app.schemes.dog import ResponseDog

class Activity(BaseModel):
    description: str

class CreateActivity(Activity):
    dog_id: int

class ResponseActivity(Activity):
    id: int
    created_at: datetime
    dog_id: int
    dog: ResponseDog

    class Config:
        from_attributes = True
