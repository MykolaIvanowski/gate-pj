from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import jwt

from config import JWT_SECRET, JWT_ALGORITHM



async def jwt_middleware(request:Request, call_next):
    if request.url.path.startswith("/auth"):
        return await call_next(request)
    token = request.headers.get("Authorisation")

    if not token:
        return JSONResponse({"detail": "token is missing"}, status_code=401)

    try:
        token =  token.replace("Bearer ", "")
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        request.state.user = payload
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    return  await call_next(request)