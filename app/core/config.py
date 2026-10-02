from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    FIRST_OWNER_NAME: str
    FIRST_OWNER_PHONE: str
    FIRST_OWNER_EMAIL: str
    FIRST_OWNER_PASSWORD: str

    class Config:
        env_file=".env"

settings = Settings()

