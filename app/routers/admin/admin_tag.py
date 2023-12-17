from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemes.tag import Tag, ResponseTag
from typing import Optional
from app.database.config import get_db
from app.utils import oauth2
from app import models
from sqlalchemy import func
from app.utils.roles import RoleChecker, Role
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination import Page

only_admin_allowed = RoleChecker([Role.ADMIN.value])

router = APIRouter(
    prefix="/admin/tags",
    tags=["Admin Tags"]
)

# Get all tags
@router.get('/', response_model=Page[ResponseTag], dependencies=[Depends(only_admin_allowed)])
async def admin_get_all_tags(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    tags = db.query(models.Tag).filter(models.Tag.name.contains(search.lower()))
    return paginate(db, tags)

# Create new tag
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseTag, dependencies=[Depends(only_admin_allowed)])
async def admin_create_tag(tag: Tag, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_tag = models.Tag(name=tag.name.lower())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

#delete tag
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(only_admin_allowed)])
async def admin_delete_tag(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    tag = db.query(models.Tag).filter(models.Tag.id == id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag with id {id} not found")
    db.delete(tag)
    db.commit()
    return 'done'

