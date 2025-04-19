from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


class CustomCORSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, allow_origins=None):
        super().__init__(app)
        self.allow_origins = allow_origins or ["*"]

    async def dispatch(self, request: Scope, call_next):
        response: Response = await call_next(request)

        origin = request["headers"]
        origin_value = None
        for k, v in origin:
            if k == b"origin":
                origin_value = v.decode()
                break

        if origin_value in self.allow_origins or "*" in self.allow_origins:
            response.headers["Access-Control-Allow-Origin"] = origin_value or "*"
            response.headers["Access-Control-Allow-Methods"] = (
                "GET, POST, PUT, DELETE, OPTIONS"
            )
            response.headers["Access-Control-Allow-Headers"] = (
                "Authorization, Content-Type"
            )
            response.headers["Access-Control-Allow-Credentials"] = "true"

        # Handle preflight (OPTIONS) request manually
        if request["method"] == "OPTIONS":
            return Response(status_code=204, headers=response.headers)

        return response
