from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    google_application_credentials: str
    bucket_name: str

    class Config:
        env_file = ".env"

settings = Settings()