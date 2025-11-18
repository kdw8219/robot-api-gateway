import httpx
from fastapi import Depends, Request
from fastapi.responses import Response
import app.clients.robots_client as robots_client
import app.clients.auth_client as auth_client
from app.clients.robots_client import RobotClientError
from app.clients.auth_client import AuthClientError
from app.schemas.robots import RobotCheckInput

class RobotServiceError(Exception):
    pass

class RobotAuthFailError(Exception):
    pass


#애는 Service Level Layer니까 Service에만 집중. 에러는 필요 시 의미를 컨버팅 해서 전달
async def login_service(client:httpx.AsyncClient, data:RobotCheckInput):
    #해당 서비스에서 서버에 요청을 보내는 등의 처리
    #Response 처리하여 Return
    try:
        response:Response = await robots_client.call_robot_exist(client, data=data)
        response.raise_for_status()
        
        #Robot Exist then
        
        response = await auth_client.call_auth_login(client)
        response.raise_for_status()
        
    except RobotClientError as e:
        raise RobotServiceError(e)
    
    except AuthClientError as e:
        raise RobotAuthFailError(e)
    
    return response