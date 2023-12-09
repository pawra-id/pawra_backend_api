from fastapi import FastAPI, Depends
from app.utils import oauth2
from app.routers import auth, user, dog, activity, vet, blog, analysis
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(dog.router)
app.include_router(activity.router)
app.include_router(vet.router)
app.include_router(blog.router)
app.include_router(analysis.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}