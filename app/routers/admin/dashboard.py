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

only_admin_allowed = RoleChecker([Role.ADMIN.value])

router = APIRouter(
    tags=["Admin Dashboard"],
    prefix="/dashboard"
)

@router.get("/", dependencies=[Depends(only_admin_allowed)])
async def dashboard(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #Get total users
    total_users = db.query(models.User).count()
    #Get total vets
    total_vets = db.query(models.Vet).count()
    #Get total dogs
    total_dogs = db.query(models.Dog).count()
    #Get total blogs
    total_blogs = db.query(models.Blog).count()
    #Get total activities
    total_activities = db.query(models.Activity).count()
    #Get total analysis
    total_analysis = db.query(models.Analysis).count()
    #get total actions
    total_actions = db.query(models.Actions).count()
    
    return {
        "total_users": total_users,
        "total_vets": total_vets,
        "total_dogs": total_dogs,
        "total_blogs": total_blogs,
        "total_activities": total_activities,
        "total_analysis": total_analysis,
        "total_actions": total_actions
    }