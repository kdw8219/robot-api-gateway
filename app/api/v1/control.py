from app.schemas.robots import RobotCheckInput
from app.schemas.heartbeat import HeartbeatInput, HeartbeatOutput
import app.services.control_service as control_service
from app.schemas.login import loginOutput
from app.schemas.error import ErrorOutput
import httpx
from aiokafka import AIOKafkaProducer
from fastapi import BackgroundTasks, HTTPException, status


async def command_control():
    pass