from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.schemes.analysis import ResponseAnalysis, Analysis, CreateAnalysis
from typing import List, Optional
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.utils import oauth2
from sqlalchemy import or_
from app.config import settings
from fastapi_pagination.ext.sqlalchemy import paginate
from app import models
from datetime import datetime, timedelta
from fastapi_pagination import Page
import requests

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

#get my analysis
@router.get("/", response_model=Page[ResponseAnalysis])
async def get_my_analysis(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ''):
    #only show my analysis from my dogs
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        or_(
            models.Analysis.description.contains(search.lower()),
            models.Analysis.prediction.contains(search.lower())
        ),
        models.Dog.owner_id == current_user.id
        )
    return paginate(db, analysis)

#get analysis by id
@router.get("/{id}", response_model=ResponseAnalysis)
async def get_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id, 
        models.Dog.owner_id == current_user.id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis

#create analysis
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ResponseAnalysis)
async def create_analysis(analysis: CreateAnalysis, days: int = 7, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    dog = db.query(models.Dog).filter(models.Dog.id == analysis.dog_id).first()
    #Check if dog exist
    if not dog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Dog with id {analysis.dog_id} not found')
    #check if dog belongs to user
    if dog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    #get time delta now - days
    this_time = datetime.now()
    delta = timedelta(days=days)
    last_time = this_time - delta

    #Get all activities from the last X days from the dog
    activities = db.query(models.Activity).filter(
        models.Activity.created_at >= last_time,
        models.Activity.dog_id == analysis.dog_id
    ).all()

    url = settings.ml_api_url + "/predict"
    #Send prediction request to ML API with list of activities
    response = requests.post(url, json=[activity.description for activity in activities])
    
    if response.status_code == 400:
        #return json with message activity empty
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Activity list is empty")

    #mock prediction
    ml_prediction = response.content.decode('utf-8')
    ml_description = "This is a description"

    #create analysis
    new_analysis = models.Analysis(
        prediction = ml_prediction,
        description = ml_description,
        dog_id = analysis.dog_id
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)

    created_analysis = db.query(models.Analysis).filter(models.Analysis.id == new_analysis.id).first()

    #attach activities to analysis
    created_analysis.activities.extend(activities)

    db.commit()
    db.refresh(created_analysis)

    return created_analysis

#delete analysis
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id, 
        models.Dog.owner_id == current_user.id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    db.delete(analysis)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#share analysis
@router.put("/{id}/share", status_code=status.HTTP_202_ACCEPTED)
async def share_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id, 
        models.Dog.owner_id == current_user.id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    analysis.is_shared = True
    db.commit()
    return {"message": "Analysis shared"}

#unshare analysis
@router.put("/{id}/unshare", status_code=status.HTTP_202_ACCEPTED)
async def unshare_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id, 
        models.Dog.owner_id == current_user.id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    analysis.is_shared = False
    analysis.updated_at = datetime.now()
    db.commit()

    return {"message": "Analysis unshared"}

#Get all shared analysis
@router.get("/shared", response_model=Page[ResponseAnalysis])
async def get_my_shared_analysis(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ''):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        or_(
            models.Analysis.description.contains(search.lower()),
            models.Analysis.prediction.contains(search.lower())
        ),
        models.Analysis.is_shared == True
        )
    return paginate(db, analysis)

#get analysis by my dog id (current user)
@router.get("/dog/{id}", response_model=Page[ResponseAnalysis])
async def get_analysis_by_my_dog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ''):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        or_(
            models.Analysis.description.contains(search.lower()),
            models.Analysis.prediction.contains(search.lower())
        ),
        models.Dog.id == id,
        models.Dog.owner_id == current_user.id
        )
    return paginate(db, analysis)
