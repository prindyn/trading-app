from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    notify_token: str

    class Config:
        env_file = ".env"


settings = Settings()
