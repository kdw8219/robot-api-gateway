from app.schemas.robots import RobotCheckInput
from app.schemas.heartbeat import HeartbeatInput, HeartbeatOutput
import app.services.conn_service as conn_service
from app.schemas.login import loginOutput
from app.schemas.error import ErrorOutput
import httpx
from aiokafka import AIOKafkaProducer
from fastapi import BackgroundTasks, HTTPException, status


async def login(payload:RobotCheckInput, client: httpx.AsyncClient):
    
    #최대한 simple하게 service call만
    try:
        json_data = {
            'robot_id':payload.robot_id,
            'robot_secret':payload.robot_secret
        }
        login_response = await conn_service.login_service(client, json_data)
        login_response.raise_for_status()
               
        data = login_response.json()
    except conn_service.RobotAuthFailError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication Error"
        )
    except conn_service.RobotServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Service Error"
        )
        
    
    return loginOutput(access_token=data['access_token'], refresh_token=data['refresh_token'])



async def heartbeat(payload:HeartbeatInput, backgroundTasks:BackgroundTasks, client: httpx.AsyncClient, kafka: AIOKafkaProducer):
    
    #최대한 simple하게 service call만
    try:
        json_data = {
            'robot_id':payload.robot_id,
            'stream_ip':payload.stream_ip,
        }
        heartbeat_response = await conn_service.heartbeat_service(client, kafka, backgroundTasks, json_data)
        heartbeat_response.raise_for_status()
    except conn_service.HeartbeatServiceError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Service Error"
        )
    except conn_service.HeartbeatNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not Found Exception"
        )
        
    
    return HeartbeatOutput(result='heartbeat success')


async def signaling():
    pass


async def offer_request():
    pass