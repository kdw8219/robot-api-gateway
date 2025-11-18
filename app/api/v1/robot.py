from fastapi import APIRouter, Depends, Request
from app.schemas.robots import RobotCheckInput
import app.services.robot_service as robot_service
from fastapi.responses import JSONResponse
from app.schemas.login import loginOutput
from app.schemas.error import ErrorOutput
import httpx

router = APIRouter()


def get_client(request: Request):
    return request.app.state.client

@router.post('/login')
async def login(payload:RobotCheckInput,
    client: httpx.AsyncClient = Depends(get_client)):
    
    #최대한 simple하게 service call만
    try:
        json_data = {
            'robot_id':payload.robot_id,
            'robot_secret':payload.robot_secret
        }
        login_response = await robot_service.login_service(client, json_data)
        login_response.raise_for_status()
               
        data = login_response.json()
    except robot_service.RobotAuthFailError as e:
        return ErrorOutput(message='Authentication Error')
    except robot_service.RobotServiceError as e:
        return ErrorOutput(message='Login Error')
        
    
    return loginOutput(access_token=data['access_token'], refresh_token=data['refresh_token'])