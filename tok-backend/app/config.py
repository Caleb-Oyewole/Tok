from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load key-value pairs from .env into os.environ.
# This never overrides real environment variables, so Render's env vars win in production.
load_dotenv()


class Settings(BaseSettings):
    GROQ_API_KEY: str = ""

    # No default on purpose: the value must come from .env (local) or Render's
    # Environment tab, so no credentials ever live in source code.
    DATABASE_URL: str

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        v = v.strip().strip('"').strip("'")
        if not v:
            raise ValueError(
                "DATABASE_URL is empty. Set it in .env (local) or in Render's Environment tab."
            )
        # Pin the driver explicitly. SQLAlchemy 2.1+ treats plain postgresql:// as
        # psycopg (v3), but requirements.txt installs psycopg2-binary.
        for prefix in ("postgres://", "postgresql://"):
            if v.startswith(prefix):
                return "postgresql+psycopg2://" + v[len(prefix):]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()  # type: ignore[call-arg]