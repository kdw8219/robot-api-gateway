import httpx
from fastapi.responses import Response
from fastapi import BackgroundTasks
import app.clients.robots_client as robots_client
import app.clients.auth_client as auth_client
import app.clients.robots_client as robot_client
import app.clients.robot_stats_client as robot_stats_client
from app.clients.robots_client import RobotClientError
from app.clients.auth_client import AuthClientError
from app.clients.robot_stats_client import HeartbeatClientError,HeartbeatNotFoundError
from app.schemas.robots import RobotCheckInput
from app.schemas.heartbeat import HeartbeatInput
import datetime
from aiokafka import AIOKafkaProducer
from app.core.config import get_settings

settings = get_settings()

class RobotServiceError(Exception):
    pass

class RobotAuthFailError(Exception):
    pass

class HeartbeatServiceError(Exception):
    pass

class HeartbeatUserNotFoundError(Exception): # 404 Not found
    pass

async def send_kafka_heartbeat(kafka:AIOKafkaProducer, robot_id:str, nowtime:str):
    try:
        topic = settings.HEARTBEAT_TOPIC
        payload = {
            'robot_id':robot_id,
            'timestamp':nowtime
        }
        result =await kafka.send_and_wait(topic, payload)
        
        print(f"Complete...: Topic={result.topic}, Partition={result.partition}, Offset={result.offset}")
        
    except Exception as e:
        print(e)
    

async def heartbeat_service(client:httpx.AsyncClient, kafka: AIOKafkaProducer, backgroundTasks:BackgroundTasks, data:HeartbeatInput):
    #해당 서비스에서 서버에 요청을 보내는 등의 처리
    #Response 처리하여 Return
    try:
        response:Response = await robot_client.call_robot_exist(client, data=data)
        response.raise_for_status()
        
        #using kafka to send data
        timestamp = datetime.datetime.now().isoformat()
        backgroundTasks.add_task(send_kafka_heartbeat, kafka, data['robot_id'], timestamp) # 별도 스레드 동작
        
    except HeartbeatClientError as e:
        raise HeartbeatServiceError(e)
    
    except HeartbeatNotFoundError as e:
        raise HeartbeatUserNotFoundError(e)
    
    return response

#애는 Service Level Layer니까 Service에만 집중. 에러는 필요 시 의미를 컨버팅 해서 전달
async def login_service(client:httpx.AsyncClient, data:RobotCheckInput):
    #해당 서비스에서 서버에 요청을 보내는 등의 처리
    #Response 처리하여 Return
    try:
        response:Response = await robots_client.call_robot_login(client, data=data)
        response.raise_for_status()
        
        #Robot Exist then
        
        response = await auth_client.call_auth_login(client)
        response.raise_for_status()
        
    except RobotClientError as e:
        raise RobotServiceError(e)
    
    except AuthClientError as e:
        raise RobotAuthFailError(e)
    
    return response