from fastapi import APIRouter

router = APIRouter(
    tags=["Authentication"],
)

@router.get("/token")
async def login():
    return {"message": "Hello World"}