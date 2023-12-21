from pydantic import BaseModel
from datetime import datetime
import pytz

class Action(BaseModel):
    action: str
    description: str

class ResponseAction(Action):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True