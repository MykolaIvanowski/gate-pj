import time
from fastapi import Request
from fastapi.responses import JSONResponse
import redis

redis_db = redis.Redis(host='localhost', port=6379, db=0)

LIMIT_GET = 100          # GET limit
LIMIT_WRITE = 20          # POST/PUT/DELETE limit
WINDOW = 60               # seconds


async def rate_limit_middleware(request: Request, call_next):
    now = time.time()
    ip = request.client.host

    user_id = None
    if hasattr(request.state, "user"):
        user_id = request.state.user.get("sub") or request.state.user.get("user_id")

    identity = user_id or ip

    if request.method in ("PUT", "POST", "DELETE"):
        limit = LIMIT_WRITE
        key = f"rate:write:{identity}"
    else:
        limit = LIMIT_GET
        key = f"rate:get:{identity}"

    pipeline = redis_db.pipeline()
    pipeline.zadd(key, {now: now})
    pipeline.zremrangebyscore(key, 0, now - WINDOW)
    pipeline.zcard(key)
    pipeline.expire(key, WINDOW)

    _, _, count, _ = pipeline.execute()

    if count >= limit:
        oldest = redis_db.zrange(key, 0, 0, withscores=True)
        if oldest:
            retry_after = WINDOW - (now - oldest[0][1])
        else:
            retry_after = WINDOW

        return JSONResponse(
            {
                "detail": "Rate limit exceeded",
                "limit": limit,
                "window_seconds": WINDOW,
                "retry_after_seconds": round(retry_after, 2)
            },
            status_code=429
        )

    return await call_next(request)
