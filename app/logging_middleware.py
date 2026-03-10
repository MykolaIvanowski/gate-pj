import time
from binascii import a2b_qp
from http.client import responses

from fastapi import Request


async def logging_middleware(request: Request, call_next):
    start  = time.time()
    response  = await call_next(request)
    duration = round((time.time()-start)*1000,2)

    print(f"method: {request.method} path {request.url.path} status {response.status_code} duration [{duration}ms]")

    return response