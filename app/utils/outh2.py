from fastapi.security import OAuth2PasswordBearer
from app.config import settings as s

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

SECRET_KEY = s.secret_key
ALGORITHM = s.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = s.access_token_expire_minutes

#Create token
def create_token(data: dict):
    pass

#Verify login

#Get current logged in user
