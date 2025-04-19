import app.core.logging
from app.middleware.security import CustomCORSMiddleware
from app.middleware.exception_handler import ExceptionLoggingMiddleware
from fastapi import FastAPI
from app.routes.proxy import router as proxy_router
from app.routes.openapi import router as openapi_router

app = FastAPI(title="API Gateway", openapi_url=None, redoc_url=None)

app.add_middleware(ExceptionLoggingMiddleware)
app.add_middleware(CustomCORSMiddleware, allow_origins=["http://localhost:3000"])

app.include_router(openapi_router, tags=["OpenAPI"])
app.include_router(proxy_router, tags=["API-Gateway"])
