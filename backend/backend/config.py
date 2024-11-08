from pydantic_settings import BaseSettings
from dotenv import find_dotenv

class Settings(BaseSettings):

    class Config:
        env_file = find_dotenv(".env")

    POSTGRES_USER:str 
    POSTGRES_PASSWORD:str
    secret_key:str

settings = Settings()
