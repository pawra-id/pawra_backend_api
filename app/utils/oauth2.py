from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status, HTTPException
from datetime import datetime, timedelta
from app.config import settings as s
from sqlalchemy.orm import Session
from app.database.config import get_db
from jose import jwt, JWTError
from app.schemes.token import TokenData
from app import models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = s.secret_key
ALGORITHM = s.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = s.access_token_expire_minutes

#Create token
def create_token(data: dict):
    #copy data
    to_encode = data.copy()

    #set expiration time
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #add expiration time to data
    to_encode.update({"exp": expire})
    #encode data
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    #return encoded data
    return encoded_jwt

#Verify login
def verify_access_token(token: str, credentials_exception):
    try:
        #decode token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        #get user id from decoded token
        id: str = payload.get('user_id')
        #if id is None, raise exception
        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
    except JWTError:
        raise credentials_exception
    #return token data
    return token_data

#Get current logged in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    #make custom exception
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #verify token
    token = verify_access_token(token, credentials_exception)
    #get logged in user
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
