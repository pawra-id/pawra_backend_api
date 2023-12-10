from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from app.schemes.blog import ResponseBlog, Blog
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.utils import oauth2
from app import models
from app.utils.gcs import GCStorage
from fastapi_pagination import Page
from sqlalchemy import or_
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

#Get all blogs
@router.get("/", response_model=Page[ResponseBlog])
async def get_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    blogs = db.query(models.Blog).filter(
        or_(
            models.Blog.title.contains(search.lower()),
            models.Blog.content.contains(search.lower()),
        ))
    return paginate(db, blogs)

#Get blog by id
@router.get("/{id}", response_model=ResponseBlog)
async def get_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.author_id == current_user.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog doesnt exist")
    return blog

