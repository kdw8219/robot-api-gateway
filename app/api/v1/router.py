from fastapi import APIRouter, Depends, Request, BackgroundTasks
from app.schemas.robots import RobotCheckInput
from app.schemas.heartbeat import HeartbeatInput
import httpx
from aiokafka import AIOKafkaProducer
import app.api.v1.connection as robot_connection
import app.api.v1.control as robot_control

router = APIRouter()

def get_client(request: Request):
    return request.app.state.client

def get_kafka(request: Request):
    return request.app.state.kafka

@router.post('/login')
async def route_login(payload:RobotCheckInput,
    client: httpx.AsyncClient = Depends(get_client)):
    
    return await robot_connection.login(payload, client)

@router.post('/heartbeat')
async def route_heartbeat(payload:HeartbeatInput,
    backgroundTasks: BackgroundTasks,
    client: httpx.AsyncClient = Depends(get_client),
    kafka: AIOKafkaProducer = Depends(get_kafka)):
    
    return await robot_connection.heartbeat(payload, backgroundTasks, client, kafka)


@router.post('/control')
async def robot_control():
    
    return await robot_control.command_control()
    
    
@router.post('/offer-request')
async def robot_rtc_request():
    
    return await robot_connection.offer_request()

@router.post('/signaling')
async def robot_rtc_signaling():
    
    return await robot_connection.signaling()