from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(
        env_file=['.env', '../.env'],
        env_file_encoding='utf-8',
        extra="allow",
        case_sensitive=False,
    )

    API_VERSION: str
    MODE: str = 'prod'
    R2_BASE_URL: str


settings = Settings()
