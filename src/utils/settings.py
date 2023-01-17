from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USERNAME: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_NAME: str = 'idotpet'
    DB_PORT: int = 5432

    JWT_SECRET: str = 'abcdefgh'
    JWT_TOKEN_EXPIRE_MINUTES: int = 60*24*7
    JWT_ALGORITHM: str = 'HS256'

    BASE_API_URL: str = 'localhost:8000'


settings = Settings()
