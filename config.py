from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    database_name: str
    database_username: str
    database_password: str
    database_port: str
    database_hostname: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    base_url: str
    api_key: str
    session_key: str

    class Config:
        env_file = ".env"


settings = Settings()
