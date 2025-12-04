
from app.core.config import get_settings
from aiokafka import AIOKafkaProducer

settings = get_settings()

class HeartbeatClientError(Exception):
    pass

class HeartbeatNotFoundError(Exception):
    pass

async def send_kafka_heartbeat(kafka:AIOKafkaProducer, robot_id:str, nowtime:str, stream_ip:str):
    try:
        topic = settings.HEARTBEAT_TOPIC
        payload = {
            'robot_id':robot_id,
            'is_alive':True,
            'stream_ip':stream_ip,
            'timestamp':nowtime
        }
        result =await kafka.send_and_wait(topic, payload)
        
        print(f"Complete...: Topic={result.topic}, Partition={result.partition}, Offset={result.offset}")
        
    except Exception as e:
        raise HeartbeatClientError(e)