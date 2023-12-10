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
from app.utils.roles import RoleChecker, Role

only_admin_allowed = RoleChecker([Role.ADMIN.value])

router = APIRouter(
    prefix="/admin/analysis",
    tags=["Admin Analysis"]
)

#get all analysis (admin)
@router.get("/", response_model=Page[ResponseAnalysis], dependencies=[Depends(only_admin_allowed)])
async def admin_get_all_analysis(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ''):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        or_(
            models.Analysis.description.contains(search.lower()),
            models.Analysis.prediction.contains(search.lower())
        ),
        )
    return paginate(db, analysis)

#get analysis by id
@router.get("/{id}", response_model=ResponseAnalysis, dependencies=[Depends(only_admin_allowed)])
async def admin_get_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    return analysis

#delete analysis
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(only_admin_allowed)])
async def admin_delete_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    db.delete(analysis)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#share analysis
@router.put("/{id}/share", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(only_admin_allowed)])
async def admin_share_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    analysis.is_shared = True
    db.commit()
    return {"message": "Analysis shared"}

#unshare analysis
@router.put("/{id}/unshare", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(only_admin_allowed)])
async def admin_unshare_analysis(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        models.Analysis.id == id).first()
    
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not found")
    
    analysis.is_shared = False
    analysis.updated_at = datetime.now()
    db.commit()

    return {"message": "Analysis unshared"}

#get analysis by dog id (admin)
@router.get("/dog/{id}", response_model=Page[ResponseAnalysis], dependencies=[Depends(only_admin_allowed)])
async def admin_get_analysis_by_dog(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), search: Optional[str] = ''):
    analysis = db.query(models.Analysis).join(models.Dog).filter(
        or_(
            models.Analysis.description.contains(search.lower()),
            models.Analysis.prediction.contains(search.lower())
        ),
        models.Dog.id == id
        )
    return paginate(db, analysis)