from fastapi import APIRouter, Depends, HTTPException, status
from app.schemes.user import ResponseUser, CreateUser
from sqlalchemy.orm import Session
from app import models
from app.utils import oauth2
from app.utils.crypt import hash
from app.database.config import get_db

router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    #hasing password
    user.password = hash(user.password)

    #get data from user schema, dump it to model, then pass it to db
    new_user = models.User(**user.model_dump())

    #add to db
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=ResponseUser)
async def get_user(id: int, db: Session = Depends(get_db)):
    #get user by id
    user = db.query(models.User).filter(models.User.id == id).first()
    #if user doesnt exist
    if not user:
        #raise error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist")
    return user

@router.put('/{id}', response_model=ResponseUser)
async def update_user(id: int, user: CreateUser, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get user by id
    user_update = db.query(models.User).filter(models.User.id == id)
    #check if user exists
    if not user_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesnt exist")
    
    #update user
    user_update.update(user.model_dump())
    db.commit()
    db.refresh(user_update.first())

    return user_update.first()
