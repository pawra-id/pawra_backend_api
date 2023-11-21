from fastapi import FastAPI, Depends
from app.utils import oauth2
from app.routers import auth, user, dog, activity, vet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dog.router)
app.include_router(activity.router)
app.include_router(vet.router)

@app.get("/")
async def root(current_user: int = Depends(oauth2.get_current_user)):
    return {"message": "Hello World"}