from fastapi import Request
from fastapi.responses import JSONResponse
import redis


redis_db = redis.Redis(host='localhost', port=6379,db=0)

RATE_LIMIT = 100
WINDOW = 60

async def rate_limit_middleware(request:Request, call_next):
    ip = request.client.host

    user_id = None
    if hasattr(request.state, "user"):
        user_id = request.state.user.get("sub") or request.state.user.get("user_id")

    key = f"rate:{user_id or ip}"
    current  = redis_db.incr(key)
    if current == 1:
        redis_db.expire(key, WINDOW)


    if current > RATE_LIMIT:
        ttl = redis_db.ttl(key)
        return JSONResponse(
            {
                "detail": "you have exceeded the rate limit",
                "retry_after_seconds": ttl
            },
            status_code=429
        )
    return await call_next(request)