from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemes.dog import ResponseDog, Dog
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.utils import oauth2
from sqlalchemy import or_
from app import models

router = APIRouter(
    prefix="/dogs",
    tags=["Dogs"]
)

@router.get("/", response_model=List[ResponseDog])
async def get_dogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 15, skip: int = 0, search: Optional[str] = ""):
    #only can see their own dogs
    dogs = db.query(models.Dog).filter(
        or_(
            models.Dog.name.contains(search.lower()),
            models.Dog.breed.contains(search.lower()),
        ), 
        models.Dog.owner_id == current_user.id).limit(limit).offset(skip).all()
    return dogs

@router.get("/{id}", response_model=ResponseDog)
async def get_dog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    dog = db.query(models.Dog).filter(models.Dog.id == id, models.Dog.owner_id == current_user.id).first()
    if not dog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dog doesnt exist")
    return dog

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseDog)
async def create_dog(dog: Dog, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #lowercase the all
    dog.name = dog.name.lower()
    dog.breed = dog.breed.lower()
    dog.gender = dog.gender.lower()

    new_dog = models.Dog(owner_id=current_user.id, **dog.model_dump())
    db.add(new_dog)
    db.commit()
    db.refresh(new_dog)
    return new_dog

@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseDog)
async def update_dog(id: int, dog: Dog, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    dog_update = db.query(models.Dog).filter(models.Dog.id == id, models.Dog.owner_id == current_user.id)

    if not dog_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dog doesnt exist")
    
    dog_update.update(dog.model_dump())
    db.commit()
    db.refresh(dog_update.first())
    return dog_update.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    dog_delete = db.query(models.Dog).filter(models.Dog.id == id, models.Dog.owner_id == current_user.id)
    
    if not dog_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dog doesnt exist")
    
    dog_delete.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Dog deleted")

