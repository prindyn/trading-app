from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import Notification
from app.core.settings import settings

router = APIRouter()


@router.post("/")
async def send_notification(
    notification: Notification, token: str = Depends(lambda: settings.notify_token)
):
    # Mock sending notification
    print(f"Sending to {notification.email}: {notification.subject}")
    return {"detail": "Notification sent"}
