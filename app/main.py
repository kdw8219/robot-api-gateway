from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.v1.router import router as MainRouter
from contextlib import asynccontextmanager
import httpx
from aiokafka import AIOKafkaProducer
import json
from app.core.config import get_settings

settings = get_settings()

@asynccontextmanager
async def lifespan(app:FastAPI):
    client = httpx.AsyncClient()
    app.state.client = client
    
    kafka = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVER
                             , value_serializer=lambda m: json.dumps(m).encode('utf-8'))
    app.state.kafka = kafka
    
    await app.state.kafka.start()
    
    yield
    
    await client.aclose()
    await app.state.kafka.stop()

app = FastAPI(lifespan = lifespan)
app.include_router(MainRouter, prefix="/api/robots")

@app.exception_handler(httpx.HTTPStatusError)
async def http_status_error_handler(request: Request, exc: httpx.HTTPStatusError):
    # 에러가 발생했을 때 클라이언트에게 반환할 응답을 정의합니다.
    print(f"외부 API 요청 중 에러 발생: {exc.response.status_code}")
    return JSONResponse(
        status_code=status.HTTP_502_BAD_GATEWAY, # 502 에러로 반환
        content={"message": "외부 서비스와 통신 중 문제가 발생했습니다."},
    )
    
@app.exception_handler(httpx.ReadTimeout)
async def http_status_error_handler(request: Request, exc: httpx.ReadTimeout):
    # 에러가 발생했을 때 클라이언트에게 반환할 응답을 정의합니다.
    return JSONResponse(
        status_code=status.HTTP_504_GATEWAY_TIMEOUT, # 504 에러로 반환
        content={"message": "외부 서비스와 통신 중 타임아웃이 발생했습니다."},
    )