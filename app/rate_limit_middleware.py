import time
from fastapi import Request
from fastapi.responses import JSONResponse

RATE_LIMIT = 100
WINDOW =60
request_counts = {}


async def rate_limit_middleware(request: Request, call_next):
    ip = request.client.host
    now = time.time()

    if ip not in request_counts:
        request_counts[ip] = []


    request_counts[ip] = [ts for ts in request_counts[ip] if now -ts < WINDOW]


    if len(request_counts[ip]) >= RATE_LIMIT:
        return JSONResponse(
            {"detail":"Rate limit exceeded"},
            status_code=429
        )
    request_counts[ip].append(now)
    return await call_next(request)
