from app.middlewares.exception_handler import ExceptionLoggingMiddleware
import app.core.logging
from fastapi import FastAPI
from app.routes.trade import router as trade_router
from app.routes.taskman import router as taskman_router

app = FastAPI(title="Trade Service")

app.add_middleware(ExceptionLoggingMiddleware)

app.include_router(trade_router, prefix="/trade", tags=["Trade"])
app.include_router(taskman_router, prefix="/task", tags=["Task"])
