from pydantic_settings import BaseSettings
from pydantic import Extra

class Settings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"

    model_config = {
        "env_file": ".env",
        "extra": Extra.allow,  # Allow extra fields
    }

settings = Settings()
