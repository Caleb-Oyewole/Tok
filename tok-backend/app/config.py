import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load key-value pairs from .env file into os.environ
load_dotenv()

class Settings(BaseSettings):
    # Set default values so Pylance doesn't flag missing constructor arguments
    GROQ_API_KEY: str = ""
    DATABASE_URL: str = "postgresql://tok_user:lONDdnB9jyWqeHhsEXDnaJIbIHxFYXVW@dpg-dap6jjo0cd8s73bueq40-a.oregon-postgres.render.com/tok_db"

    # Modern Pydantic v2 configuration settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()