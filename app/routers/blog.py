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

@router.get("/", response_model=Page[ResponseBlog])
async def get_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    #only can see their own blogs
    blogs = db.query(models.Blog).filter(
        or_(
            models.Blog.title.contains(search.lower()),
            models.Blog.content.contains(search.lower()),
        ), 
        models.Blog.author_id == current_user.id)
    return paginate(db, blogs)

@router.get("/{id}", response_model=ResponseBlog)
async def get_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.author_id == current_user.id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog doesnt exist")
    return blog

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseBlog)
async def create_blog(blog: Blog, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_blog = models.Blog(author_id=current_user.id, **blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseBlog)
async def update_blog(id: int, blog: Blog, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog_update = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.author_id == current_user.id)

    if not blog_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog doesnt exist")
    
    blog_update.update(blog.model_dump())
    blog_update.update({
        'updated_at': datetime.now()
    })
    db.commit()
    db.refresh(blog_update.first())
    return blog_update.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blog_delete = db.query(models.Blog).filter(models.Blog.id == id, models.Blog.author_id == current_user.id)
    if not blog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog doesnt exist")
    blog_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/all", response_model=Page[ResponseBlog])
async def get_all_blogs(db: Session = Depends(get_db), search: Optional[str] = ""):
    blogs = db.query(models.Blog).filter(
        or_(
            models.Blog.title.contains(search.lower()),
            models.Blog.content.contains(search.lower()),
        ))
    return paginate(db, blogs)


#upload blog image
@router.post('/image', status_code=status.HTTP_200_OK)
async def upload_vet_image(file: UploadFile = File(), current_user: int = Depends(oauth2.get_current_user)):
    url  = await GCStorage().upload_file(file, 'blog_picture')
    return url
