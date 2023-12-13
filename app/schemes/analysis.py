from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List
from app.schemes.activity import ActivityForAnalysis
from app.schemes.action import ResponseAction

class Analysis(BaseModel):
    dog_id: int
    prediction: str
    description: Optional[str] = None
    is_shared: Optional[bool] = False

class CreateAnalysis(BaseModel):
    dog_id: int

class ResponseAnalysis(Analysis):
    id: int
    created_at: datetime
    updated_at: datetime
    activities: List[ActivityForAnalysis]
    actions: List[ResponseAction]

    class Config:
        from_attributes = True