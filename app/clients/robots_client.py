import httpx
from app.core.config import get_settings
from httpx import Response

settings = get_settings()

class RobotClientError(Exception):
    pass

#에러 처리 시에는 기능에만 집중하자. 애는 기능이다.
#우선 얘는 ZTL 레벨로 가면 인증'도' robot에서 해야할거다. header 데이터가 서비스마다 달라질 수 있어, Client 분리
async def call_robot_login(client: httpx.AsyncClient, data):
    url = settings.ROBOTS_URL + settings.ROBOTS_LOGIN
    response:Response | None = None
    print(url)
    try:
        response = await client.post(url, json=data, timeout= settings.ROBOTS_TIMEOUT)
        response.raise_for_status()
    
    except httpx.RequestError as e: #4x, 5x error
        raise RobotClientError(e)
    
    return response

async def call_robot_exist(client: httpx.AsyncClient, data):
    url = settings.ROBOTS_URL + data['robot_id'] + '/'
    response:Response | None = None
    print(url)
    try:
        response = await client.get(url, timeout= settings.ROBOTS_TIMEOUT)
        response.raise_for_status()
    
    except httpx.RequestError as e: #4x, 5x error
        raise RobotClientError(e)
    
    return response