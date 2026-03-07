import httpx
from fastapi import APIRouter, Request
from config import USER_SERVICE_URL, ITEMS_SERVICE_URL, AUTH_SERVICE_URL


router = APIRouter()

async def forward(request: Request, target_url: str):
    async with httpx.AsyncClient() as client:
        body  = await request.body()
        headers = dict(request.headers)

        response = await client.request(
            request.method, target_url+ request.url.path, params=request.query_params,
            content=body, headers=headers
        )
        return response

@router.api_route("/users/{path:path}", methods=["GET", "PUT", "POST", "DELETE"])
async def users_proxy(path: str, request: Request):
    return await forward(request, USER_SERVICE_URL)

@router.api_route("/items/{pat:path}", methods=["GET", "POST", "PUT", "DELETE"])
async  def item_proxy(path:str, request:Request):
    return await forward(request, ITEMS_SERVICE_URL)

@router.api_route("/auth/{path:path}", methods=["GET", "POST"])
async def auth_proxy(path:str, request:Request):
    return await forward(request, AUTH_SERVICE_URL)