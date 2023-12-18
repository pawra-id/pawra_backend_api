from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from app.schemes.user import ResponseUser, CreateUser, User
from sqlalchemy.orm import Session
from app import models
from app.utils import oauth2
from app.utils.crypt import hash
from app.database.config import get_db
from typing import List, Optional
from datetime import datetime
from app.utils.gcs import GCStorage
from fastapi_pagination import Page
from sqlalchemy import or_
from fastapi_pagination.ext.sqlalchemy import paginate
from app.utils.roles import RoleChecker, Role

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

only_admin_allowed = RoleChecker([Role.ADMIN.value])

#Get all user
@router.get(
        "/", 
        response_model=Page[ResponseUser], 
        dependencies=[Depends(only_admin_allowed)],
        )
async def admin_get_all_users(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    #get all users
    users = db.query(models.User).filter(
        or_(
            models.User.username.ilike(f"%{search}%"),
            models.User.email.ilike(f"%{search}%"),
            models.User.address.ilike(f"%{search}%"),
        )
    )

    return paginate(db, users)

#Create user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    #hasing password
    user.password = hash(user.password)

    #get data from user schema, dump it to model, then pass it to db
    new_user = models.User(**user.model_dump())

    #validate if user already exist
    if db.query(models.User).filter(models.User.email == new_user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    #validate if username already exist
    if db.query(models.User).filter(models.User.username == new_user.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    #add to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#Get user by id
@router.get("/{id}", response_model=ResponseUser)
async def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get user by id
    user = db.query(models.User).filter(models.User.id == id).first()
    #if user doesnt exist
    if not user:
        #raise error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist")
    return user

#Update user by id
@router.put('/{id}', response_model=ResponseUser)
async def update_user(id: int, user: User, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get user by id
    user_update = db.query(models.User).filter(models.User.id == id)
    #check if user exists
    if not user_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist")

    #update user
    user_update.update(user.model_dump())

    user_update.update({
        'updated_at': datetime.now()
    })
    db.commit()
    db.refresh(user_update.first())

    return user_update.first()

#upload profile picture
@router.post('/image', status_code=status.HTTP_200_OK)
async def upload_profile_picture(file: UploadFile = File(),  current_user: int = Depends(oauth2.get_current_user)):
    url  = await GCStorage().upload_file(file, 'profile_picture')

    return url