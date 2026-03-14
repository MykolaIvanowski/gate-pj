import httpx


async def check_service(url: str):
    try:
        async  with httpx.AsyncClient(timeout=1.0) as client:
            result  = await client.get(url + '/health')
            return result.status_code == 200

    except:
        return False


