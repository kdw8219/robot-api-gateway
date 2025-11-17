from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    print('get messages!')
    return {"message": "Robot API Gateway is running"}