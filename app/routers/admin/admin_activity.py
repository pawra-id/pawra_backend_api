from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from app.schemes.activity import ResponseActivity, CreateActivity
from app.database.config import get_db
from sqlalchemy.orm import Session
from app import models
from app.utils import oauth2
from datetime import datetime
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.utils.roles import RoleChecker, Role
import pytz

router = APIRouter(
    prefix="/admin/activities",
    tags=['Admin Activity']
)

only_admin_allowed = RoleChecker([Role.ADMIN.value])


#Get all activities (admin only)
@router.get('/', response_model=Page[ResponseActivity], dependencies=[Depends(only_admin_allowed)])
async def admin_get_all_activities(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: str = ''):
    #only show my activities from my dogs
    activities = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.description.ilike(f"%{search}%"),
        )
    return paginate(db, activities)

#Get activity by id (admin only)
@router.get('/{id}', response_model=ResponseActivity, dependencies=[Depends(only_admin_allowed)])
async def admin_get_activity_by_id(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    activity = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.id == id).first()
    
    if not activity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
    return activity

#Create activity (admin only)
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseActivity)
async def admin_create_activity(activity: CreateActivity, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    timezone = pytz.timezone('Asia/Jakarta')
    dog = db.query(models.Dog).filter(models.Dog.id == activity.dog_id).first()
    #Check if dog exist
    if not dog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Dog with id {activity.dog_id} not found')

    #create activity
    new_activity = models.Activity(
        description = activity.description,
        dog_id = activity.dog_id,
        created_at = datetime.now(timezone),
        updated_at = datetime.now(timezone)
    )
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)

    created_activity = db.query(models.Activity).filter(models.Activity.id == new_activity.id).first()
    #extract tags from activity request
    for tag in activity.tags:
        #check if tag exist in db
        tag_check = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
        if tag_check is None:
            #if no, create new tag with lowercase name
            new_tag = models.Tag(name=tag.name.lower(), created_at=datetime.now(timezone))
            db.add(new_tag)
            #add tag to activity
            created_activity.tags.append(new_tag)
        else:
        #else, select tag from db
            created_activity.tags.append(tag_check)
        
        
    db.commit()
    db.refresh(created_activity)

    return created_activity

#Update activity (admin only)
@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=ResponseActivity, dependencies=[Depends(only_admin_allowed)])
async def admin_update_activity(id: int, activity: CreateActivity, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    timezone = pytz.timezone('Asia/Jakarta')
    #get activity by id, dog, and owner
    activity_update = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.id == id
        )
    #check if activity exists
    if not activity_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')
    
    #update activity
    db.query(models.Activity).\
        filter(models.Activity.id == activity_update.first().id).\
        update({
            models.Activity.description: activity.description,
            models.Activity.dog_id: activity.dog_id,
            models.Activity.updated_at: datetime.now(timezone)
        })
    db.commit()
    db.refresh(activity_update.first())

    updated_activity = db.query(models.Activity).filter(models.Activity.id == activity_update.first().id).first()

    # detach all tags from activity
    updated_activity.tags.clear()
    
    # extract tags from activity request
    for tag in activity.tags:
        #check if tag exist in db
        tag_check = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
        if tag_check is None:
            #if no, create new tag
            new_tag = models.Tag(name=tag.name, created_at=datetime.now(timezone))
            db.add(new_tag)
            #add tag to activity
            updated_activity.tags.append(new_tag)
        else:
        #else, select tag from db
            updated_activity.tags.append(tag_check)
    db.commit()
            
    return updated_activity

#Delete activity (admin only)
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(only_admin_allowed)])
async def admin_delete_activity(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get activity by id, dog, and owner
    activity_delete = db.query(models.Activity).join(models.Dog).filter(
        models.Activity.id == id)
    #check if activity exists
    if not activity_delete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Activity not found')

    #delete activity
    db.query(models.Activity).\
        filter(models.Activity.id == activity_delete.first().id).\
        delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Get all activities by dog id (admin only)
@router.get('/dog/{id}', response_model=Page[ResponseActivity], dependencies=[Depends(only_admin_allowed)])
async def admin_get_activity_by_dog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: str = ''):
    #check if dog exists
    dog = db.query(models.Dog).filter(models.Dog.id == id).first()
    if not dog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Dog with id {id} not found')
    
    activities = db.query(models.Activity).filter(
        models.Activity.dog_id == id,
        models.Activity.description.contains(search.lower())
        )
    
    return paginate(db, activities)
