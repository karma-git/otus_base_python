"""
from https://github.com/karma-git/fastapi-actions-heroku

Simple FastAPI application, running on port 8080
"""
from socket import gethostname
from datetime import datetime
from uuid import uuid4
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/")
async def root():
    """Check container"""
    return {"hostname": gethostname(), "timestamp": datetime.now(), "uuid": uuid4()}


@app.get("/isalive", status_code=status.HTTP_200_OK)
async def liveness_probe():
    """Smoke test ep"""
    return {"status": "OK"}


@app.get("/ping/")
async def ping():
    return {"message": "pong"}
