from fastapi import FastAPI, Depends
from app.utils import oauth2
from app.routers import auth, user

app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
async def root(current_user: int = Depends(oauth2.get_current_user)):
    return {"message": "Hello World"}