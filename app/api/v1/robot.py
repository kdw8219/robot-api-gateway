from fastapi import APIRouter
from app.schemas.robots import LoginInput, LoginOutput
import app.services.robot_service as robot_service

router = APIRouter()

@router.post('/login', response_model=LoginOutput)
async def login(payload:LoginInput):
    
    result = await robot_service.login_request()
    
    
    
    
    return {'result':'login success'}