from typing import List, Union
from pydantic import AnyHttpUrl, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # optional project/name defaults so Settings() can be created during tests/static analysis
    PROJECT_NAME: str | None = "mood-to-makan"
    API_V1_STR: str = "/api/v1"
    # make secret optional (use SecretStr for real deployments via env)
    SECRET_KEY: SecretStr | None = None
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ALGORITHM: str = "HS256"
    
    # Postgres settings may come from environment; allow None for safe instantiation
    POSTGRES_SERVER: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    DATABASE_URL: Union[str, None] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: str | None, info) -> str:
        if isinstance(v, str):
            return v
        values = info.data
        return str(
            f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@"
            f"{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
        )

    # OpenRouter Configuration
    OPENROUTER_API_KEY: SecretStr | None = None
    OPENROUTER_MODEL: str = "google/gemini-2.0-flash-001"
    OPENROUTER_EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Gemini Configuration
    GEMINI_API_KEY: SecretStr | None = None
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    GEMINI_EMBEDDING_MODEL: str = "models/text-embedding-004"
    
    # Legacy/Optional
    OPENAI_API_KEY: SecretStr | None = None

    # S3 Settings
    S3_ACCESS_KEY: str | None = None
    S3_SECRET_KEY: str | None = None
    S3_BUCKET_NAME: str | None = None
    S3_ENDPOINT_URL: str | None = None
    S3_BASE_URL: str | None = None

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

settings = Settings()
