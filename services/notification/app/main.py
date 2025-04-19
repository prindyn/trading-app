from fastapi import FastAPI
from app.routes.notifications import router
from app.core.settings import settings

app = FastAPI(title="Notification Service")

app.include_router(router, prefix="/notifications", tags=["Notifications"])
