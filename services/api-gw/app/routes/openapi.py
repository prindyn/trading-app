from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
import httpx
from app.core.settings import settings

router = APIRouter()


@router.get("/docs", include_in_schema=False)
async def custom_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Gateway API Docs")


@router.get("/openapi.json", include_in_schema=False)
async def aggregated_openapi():
    async with httpx.AsyncClient() as client:
        user_response = await client.get(f"{settings.user_service_url}/openapi.json")
        trade_response = await client.get(f"{settings.trade_service_url}/openapi.json")

    user_schema = user_response.json()
    trade_schema = trade_response.json()

    return {
        "openapi": "3.0.0",
        "info": {"title": "API Gateway", "version": "1.0.0"},
        "paths": {**user_schema.get("paths", {}), **trade_schema.get("paths", {})},
        "components": {
            "schemas": {
                **user_schema.get("components", {}).get("schemas", {}),
                **trade_schema.get("components", {}).get("schemas", {}),
            }
        },
    }
