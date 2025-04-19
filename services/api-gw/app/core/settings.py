from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user_service_url: str
    trade_service_url: str
    notify_service_url: str

    class Config:
        env_file = ".env"


settings = Settings()
