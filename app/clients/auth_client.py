import httpx
from app.core.config import get_settings
from httpx import Response

settings = get_settings()

class AuthClientError(Exception):
    pass

#에러 처리 시에는 기능에만 집중하자. 애는 기능이다.
async def call_auth_login(client: httpx.AsyncClient):
    url = settings.AUTH_URL
    response:Response | None = None
    
    try:
        print(url)
        response = await client.post(url, json={}, timeout= settings.AUTH_TIMEOUT)
        response.raise_for_status()
    
    except httpx.HTTPError as e: #4x, 5x error
        raise AuthClientError(e)
    
    return response 