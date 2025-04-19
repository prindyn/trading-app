from pydantic import BaseModel


class Notification(BaseModel):
    email: str
    subject: str
    message: str
