from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.config import get_db
from app.utils.crypt import verify
from app.utils.oauth2 import create_token
from sqlalchemy import or_
from app import models
from app.config import settings as s
from app.schemes.token import Token
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

router = APIRouter(
    tags=["Authentication"],
)

@router.post("/token", response_model=Token)
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm only has 2 keys: username and password
    #in this case we pass email into the username key
    user = db.query(models.User).\
        filter(
            or_(
                models.User.email == user_cred.username,
                models.User.username == user_cred.username
            )
        ).first()

    if not user:
        #check if user exists
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User doesnt exist")
    
    if not verify(user_cred.password, user.password):
        #check if password is correct
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    
    #create access token
    access_token = create_token(data={"user_id": user.id})
    #set expiration time
    expire = str(datetime.now(ZoneInfo("Asia/Jakarta")) + timedelta(minutes=s.access_token_expire_minutes))

    #get logged in user
    logged_in_user = db.query(models.User).filter(models.User.id == user.id).first()

    #remove password attribute from user
    logged_in_user.password = None

    return {"access_token": access_token, "expires_in": expire, "token_type": "bearer", "user": logged_in_user}