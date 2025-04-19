from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import httpx
import logging

from app.core.settings import settings

router = APIRouter()
logger = logging.getLogger(__name__)

# Mapping prefixes to service base URLs
SERVICE_MAP = {
    "auth": f"{settings.user_service_url}/auth",
    "user": f"{settings.user_service_url}/user",
    "trade": f"{settings.trade_service_url}/trade",
    "task": f"{settings.trade_service_url}/task",
}


async def proxy_request(request: Request, target_base: str, path: str) -> JSONResponse:
    url = f"{target_base}/{path}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers={k.decode(): v.decode() for k, v in request.headers.raw},
                content=await request.body(),
                params=dict(request.query_params),
            )

        content_type = response.headers.get("content-type", "")

        if "application/json" in content_type:
            try:
                data = response.json()

                # if pagination detected: data + total keys
                if isinstance(data, dict) and "data" in data and "total" in data:
                    return JSONResponse(content=data, status_code=response.status_code)

                # fallback if it's just a list or other valid JSON
                return JSONResponse(content=data, status_code=response.status_code)

            except Exception as e:
                logger.warning(f"Invalid JSON from upstream {url}: {e}")
                return JSONResponse(
                    content={"detail": "Invalid JSON from upstream service."},
                    status_code=502,
                )
        else:
            # non-JSON response
            return JSONResponse(
                content={
                    "detail": "Upstream service returned non-JSON response.",
                    "status_code": response.status_code,
                    "text": response.text,
                },
                status_code=response.status_code,
            )

    except httpx.RequestError as e:
        logger.error(f"Proxy request to {url} failed: {e}")
        return JSONResponse(
            status_code=502,
            content={
                "detail": "Failed to contact upstream service.",
                "error": str(e),
            },
        )


# Dynamically create proxy routes
for prefix, target_base in SERVICE_MAP.items():
    route_path = f"/{prefix}/{{path:path}}"

    async def proxy_handler(
        request: Request, path: str, target_base=target_base
    ):  # default value binds correctly in loop
        return await proxy_request(request, target_base, path)

    router.add_api_route(
        route_path,
        proxy_handler,
        methods=["GET", "POST", "PUT", "DELETE"],
        name=f"proxy_{prefix}",
    )
