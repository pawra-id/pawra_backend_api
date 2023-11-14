from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from app.schemes.activity import ResponseActivity, CreateActivity
from app.database.config import get_db
from sqlalchemy.orm import Session
from app import models
from app.utils import oauth2

router = APIRouter(
    prefix="/activities",
    tags=['Activity']
)

@router.get('/', response_model=List[ResponseActivity])
async def get_activities(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 15, skip: int = 0, search: str = ''):
    #only show my activities from my dogs
    activities = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.description.contains(search.lower()),
        models.Dog.owner_id == current_user.id
        ).limit(limit).offset(skip).all()
    return activities

@router.get('/{id}', response_model=ResponseActivity)
async def get_activity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    activity = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.id == id, 
        models.Dog.owner_id == current_user.id).first()
    
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
    return activity

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseActivity)
async def create_activity(activity: CreateActivity, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    dog = db.query(models.Dog).filter(models.Dog.id == activity.dog_id).first()
    #Check if dog exist
    if not dog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Dog with id {activity.dog_id} not found')
    #check if dog belongs to user
    if dog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    new_activity = models.Activity(**activity.model_dump())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    return new_activity

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ResponseActivity)
async def update_activity(id: int, activity: CreateActivity, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get activity by id, dog, and owner
    activity_update = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.id == id, 
        models.Dog.owner_id == current_user.id)
    #check if activity exists
    if not activity_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
    
    #update activity
    db.query(models.Activity).\
        filter(models.Activity.id == activity_update.first().id).\
        update(activity.model_dump())
    db.commit()
    db.refresh(activity_update.first())
    return activity_update.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_activity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get activity by id, dog, and owner
    activity_delete = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.id == id, 
        models.Dog.owner_id == current_user.id)
    #check if activity exists
    if not activity_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
    
    #delete activity
    db.query(models.Activity).\
        filter(models.Activity.id == activity_delete.first().id).\
        delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/dog/{id}', response_model=List[ResponseActivity])
async def get_activity_by_dog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 15, skip: int = 0, search: str = ''):
    #check if dog exists
    dog = db.query(models.Dog).filter(models.Dog.id == id).first()
    if not dog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Dog with id {id} not found')
    #check if dog belongs to user
    if dog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    activities = db.query(models.Activity).filter(
        models.Activity.dog_id == id,
        models.Activity.description.contains(search.lower())
        ).limit(limit).offset(skip).all()
    return activities
