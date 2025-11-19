
import httpx
from app.core.config import get_settings
from httpx import Response

settings = get_settings()

class HeartbeatClientError(Exception):
    pass

class HeartbeatNotFoundError(Exception):
    pass

async def send_heartbeat(client:httpx.AsyncClient, data):
    url = settings.ROBOT_STATS_URL + settings.ROBOT_STATS_HEARTBEAT
    response:Response | None = None
    print(url)
    try:
        response = await client.post(url, json=data, timeout= settings.ROBOTS_TIMEOUT)
        response.raise_for_status()
    
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HeartbeatNotFoundError(e)
        else:
            raise HeartbeatClientError(e)
            
    except httpx.RequestError as e: #4x, 5x error
        raise HeartbeatClientError(e)
    
    return response