from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemes.action import ResponseAction, Action
from app.database.config import get_db
from app import models
from app.utils import oauth2
from datetime import datetime
from typing import List
from app.utils.roles import RoleChecker, Role

only_admin_allowed = RoleChecker([Role.ADMIN.value])

router = APIRouter(
    prefix="/actions",
    tags=['Admin Action']
)

@router.get('/', response_model=List[ResponseAction], dependencies=[Depends(only_admin_allowed)])
async def admin_get_actions(db: Session = Depends(get_db)):
    actions = db.query(models.Actions).all()
    return actions

#get a single action (admin)
@router.get('/{id}', response_model=ResponseAction, dependencies=[Depends(only_admin_allowed)])
async def admin_get_action(id: int, db: Session = Depends(get_db)):
    action = db.query(models.Actions).filter(models.Actions.id == id).first()
    if not action:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Action with id {id} not found')
    return action

#create action (admin)
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ResponseAction, dependencies=[Depends(only_admin_allowed)])
async def admin_create_action(action: Action, db: Session = Depends(get_db)):
    action = models.Actions(
        action=action.action,
        description=action.description,
    )
    db.add(action)
    db.commit()
    db.refresh(action)
    return action

#update action (admin)
@router.put('/{id}', response_model=ResponseAction, dependencies=[Depends(only_admin_allowed)])
async def admin_update_action(id: int, action: Action, db: Session = Depends(get_db)):
    action = db.query(models.Actions).filter(models.Actions.id == id)
    if not action.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Action with id {id} not found')
    action.update({
        'action': action.action,
        'description': action.description,
        'updated_at': datetime.now()
    })
    db.commit()
    return action.first()

#delete action (admin)
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(only_admin_allowed)])
async def admin_delete_action(id: int, db: Session = Depends(get_db)):
    action = db.query(models.Actions).filter(models.Actions.id == id)
    if not action.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Action with id {id} not found')
    action.delete(synchronize_session=False)
    db.commit()
    return 'done'