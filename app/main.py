from fastapi import FastAPI
from router import router
from jwt_middleware import jwt_middleware
from logging_middleware import logging_middleware



app = FastAPI(title="gateway fast api pj")

app.middleware('http')(logging_middleware)
app.middleware("http")(jwt_middleware)
app.include_router(router)