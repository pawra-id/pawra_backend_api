from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.database.config import get_db
from app.utils.crypt import verify
from app.utils.outh2 import create_access_token
from app import models

router = APIRouter(
    tags=["Authentication"],
)

@router.get("/token")
async def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    #OAuth2PasswordRequestForm only has 2 keys: username and password
    #in this case we pass email into the username key
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()

    if not user:
        #check if user exists
        raise HTTPException(status=status.HTTP_403_FORBIDDEN, detail="User doesnt exist")
    
    if not verify(user_cred.password, user.password):
        #check if password is correct
        raise HTTPException(status=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    
    #create access token
    access_token = create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}