from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemes.vet import ResponseVet, Vet
from sqlalchemy.orm import Session
from app.database.config import get_db
from app import models
from typing import List
from app.utils import oauth2

router = APIRouter(
    tags=["Vets"],
    prefix="/vets"
)

@router.get("/", response_model=List[ResponseVet])
async def get_vets(db: Session = Depends(get_db), limit: int = 15, skip: int = 0, search: str = "", current_user: int = Depends(oauth2.get_current_user)):
    #get all vets
    vets = db.query(models.Vet).\
        filter(models.Vet.name.contains(search.lower())).\
        limit(limit).offset(skip).\
        all()
    return vets

@router.get("/{id}", response_model=ResponseVet)
async def get_vet(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get vet by id
    vet = db.query(models.Vet).filter(models.Vet.id == id).first()
    #if vet doesnt exist
    if not vet:
        #raise error
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vet doesnt exist")
    return vet

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseVet)
async def create_vet(vet: Vet, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get data from vet schema, dump it to model, then pass it to db
    new_vet = models.Vet(**vet.model_dump())

    #add to db
    db.add(new_vet)
    db.commit()
    db.refresh(new_vet)

    return new_vet

@router.put('/{id}', response_model=ResponseVet, status_code=status.HTTP_202_ACCEPTED)
async def update_vet(id: int, vet: Vet, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #get vet by id
    vet_update = db.query(models.Vet).filter(models.Vet.id == id)
    #check if vet exists
    if not vet_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vet doesnt exist")
    
    #update vet
    vet_update.update(vet.model_dump())
    db.commit()
    db.refresh(vet_update.first())

    return vet_update.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
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
