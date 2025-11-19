from fastapi import APIRouter, Depends, Request, BackgroundTasks
from app.schemas.robots import RobotCheckInput
from app.schemas.heartbeat import HeartbeatInput
import httpx
from aiokafka import AIOKafkaProducer
import app.api.v1.robot as robot_api

router = APIRouter()

def get_client(request: Request):
    return request.app.state.client

def get_kafka(request: Request):
    return request.app.state.kafka

@router.post('/login')
async def route_login(payload:RobotCheckInput,
    client: httpx.AsyncClient = Depends(get_client)):
    
    return await robot_api.login(payload, client)

@router.post('/heartbeat')
async def route_heartbeat(payload:HeartbeatInput,
    backgroundTasks: BackgroundTasks,
    client: httpx.AsyncClient = Depends(get_client),
    kafka: AIOKafkaProducer = Depends(get_kafka)):
    
    return await robot_api.heartbeat(payload, backgroundTasks, client, kafka)