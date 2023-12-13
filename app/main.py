from fastapi import FastAPI, Depends
from app.utils import oauth2
from app.routers import auth, user, tag, dog, activity, vet, blog, analysis
from app.routers.admin import admin_dog, admin_activity, admin_tag, admin_vets, admin_blog, admin_analysis, admin_action
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
app.include_router(admin_dog.router)

app.include_router(activity.router)
app.include_router(admin_activity.router)

app.include_router(vet.router)
app.include_router(admin_vets.router)

app.include_router(blog.router)
app.include_router(admin_blog.router)

app.include_router(analysis.router)
app.include_router(admin_analysis.router)

app.include_router(tag.router)
app.include_router(admin_tag.router)

app.include_router(admin_action.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}