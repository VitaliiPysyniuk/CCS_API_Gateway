from fastapi import FastAPI, Request

from .core import route

app = FastAPI()


@app.middleware("http")
async def process_request(request: Request, *args):
    response = await route(request)
    return response
