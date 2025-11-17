from fastapi import FastAPI
from app.api.v1.robot import router as RobotRouter
from app.api.v1.root import router as RootRouter

app = FastAPI()

app.include_router(RootRouter, prefix="")
app.include_router(RobotRouter, prefix="/api/robots")