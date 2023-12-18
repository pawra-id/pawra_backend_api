from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemes.tag import Tag, ResponseTag
from typing import List
from app.database.config import get_db
from app.utils import oauth2
from app import models
from sqlalchemy import func

router = APIRouter(
    prefix="/tags",
    tags=["Tags"]
)

@router.get('/', response_model=List[ResponseTag])
async def search_tags(search: str = "", db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tags = db.query(models.Tag).filter(
        models.Tag.name.ilike(f"%{search}%")
        ).all()
    return tags

@router.get('/most_used', response_model=List[ResponseTag])
async def get_most_used_tags(limit: int = 5, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get activities count of tag with id 1
    tags = db.query(models.Tag).\
        join(models.Tag.activities).\
            group_by(models.Tag.id).\
                order_by(func.count(models.Activity.id).\
                         desc()).limit(limit).all()
    return tags
