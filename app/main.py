from fastapi import FastAPI

from app.config import USER_SERVICE_URL, ITEMS_SERVICE_URL, AUTH_SERVICE_URL
from app.healthcheck import check_service
from router import router
from jwt_middleware import jwt_middleware
from logging_middleware import logging_middleware



app = FastAPI(title="gateway fast api pj")

app.middleware('http')(logging_middleware)
app.middleware("http")(jwt_middleware)
app.include_router(router)


@app.get("/gateway/health")
async def gateway_health():
    return {
        "user_service": await check_service(USER_SERVICE_URL),
        "items_service": await check_service(ITEMS_SERVICE_URL),
        "auth_service": await check_service(AUTH_SERVICE_URL),
    }
