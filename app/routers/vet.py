from fastapi import APIRouter, Depends, HTTPException, status, Response, File, UploadFile
from app.utils.gcs import GCStorage
from app.schemes.vet import ResponseVet, Vet
from sqlalchemy.orm import Session
from app.database.config import get_db
from app import models
from typing import List, Optional
from app.utils import oauth2
from fastapi_pagination import Page
from sqlalchemy import or_
from fastapi_pagination.ext.sqlalchemy import paginate
from datetime import datetime

router = APIRouter(
    tags=["Vets"],
    prefix="/vets"
)

@router.get("/", response_model=Page[ResponseVet])
async def get_vets(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ""):
    # get all vets
    vets = db.query(models.Vet).filter(
        or_(
            models.Vet.name.ilike(f"%{search}%"),
            models.Vet.address.ilike(f"%{search}%"),
            models.Vet.phone.ilike(f"%{search}%"),
            models.Vet.email.ilike(f"%{search}%"),
            models.Vet.clinic_name.ilike(f"%{search}%"),
        )
    )
    return paginate(db, vets)

@router.get("/{id}", response_model=ResponseVet)
async def get_vet(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get vet by id
    vet = db.query(models.Vet).filter(models.Vet.id == id).first()
    #if vet doesnt exist
    if not vet:
        #raise error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vet doesnt exist")
    return vet

#upload vet profile picture
@router.post("/image", status_code=status.HTTP_200_OK)
async def upload_vet_image(file: UploadFile = File(), current_user: int = Depends(oauth2.get_current_user)):

    url  = await GCStorage().upload_file(file, 'vet_picture')
    return url