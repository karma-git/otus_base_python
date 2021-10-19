"""
Simple FastAPI application, running on port 8080
"""
from os import environ
from socket import gethostname
from datetime import datetime
from uuid import uuid4
from fastapi import FastAPI, status
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    """Check container"""
    return {"hostname": gethostname(), "timestamp": datetime.now(), "uuid": uuid4()}


@app.get("/isalive", status_code=status.HTTP_200_OK)
async def liveness_probe():
    """Smoke test ep"""
    return {"status": "OK"}


@app.get("/version")
async def version():
    return {
        "commitAuthor": "__CI_COMMIT_AUTHOR__",
        "commitShortSHA": "__CI_COMMIT_SHORT_SHA__",
        "pipelineID": "__CI_PIPELINE_ID__",
        "gitTag": environ.get("CI_TAG", "__CI_COMMIT_TAG__"),
    }


if __name__ == "__main__":
    port = int(environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, log_level="info")
