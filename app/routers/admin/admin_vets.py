from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from app.utils.gcs import GCStorage
from app.schemes.vet import ResponseVet, Vet
from sqlalchemy.orm import Session
from app.database.config import get_db
from app import models
from typing import List
from app.utils import oauth2
from fastapi_pagination import Page
from sqlalchemy import or_
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime
from app.utils.roles import RoleChecker, Role
import pytz

only_admin_allowed = RoleChecker([Role.ADMIN.value])

router = APIRouter(
    tags=["Admin Vets"],
    prefix="/vets"
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseVet, dependencies=[Depends(only_admin_allowed)])
async def create_vet(vet: Vet, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    timezone = pytz.timezone('Asia/Jakarta')
    #get data from vet schema, dump it to model, then pass it to db
    new_vet = models.Vet(**vet.model_dump(), created_at=datetime.now(timezone), updated_at=datetime.now(timezone))

    #add to db
    db.add(new_vet)
    db.commit()
    db.refresh(new_vet)

    return new_vet

@router.put('/{id}', response_model=ResponseVet, status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(only_admin_allowed)])
async def update_vet(id: int, vet: Vet, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    timezone = pytz.timezone('Asia/Jakarta')
    #get vet by id
    vet_update = db.query(models.Vet).filter(models.Vet.id == id)
    #check if vet exists
    if not vet_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vet doesnt exist")
    
    #update vet
    vet_update.update(vet.model_dump())
    vet_update.update({
        'updated_at': datetime.now(timezone)
    })
    db.commit()
    db.refresh(vet_update.first())

    return vet_update.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(only_admin_allowed)])
async def delete_vet(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get vet by id
    vet = db.query(models.Vet).filter(models.Vet.id == id)
    #check if vet exists
    if not vet.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vet doesnt exist")
    
    #delete vet
    vet.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT, content="Vet deleted")
