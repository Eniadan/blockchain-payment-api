from pydantic_settings import BaseSettings, SettingsConfigDict

# Central configuration class for the application.
# Values can be loaded from environment variables or the .env file.
class Settings(BaseSettings):
    # Name displayed or used by the application.
    app_name: str = "Blockchain Payment API"
    # Controls whether the application runs in debug mode.
    # This should normally be disabled in production.
    debug: bool = True
    # Database connection URL loaded from the environment.
    # We don't hard-code database credentials or connection details here.
    database_url: str
    # Configure Pydantic Settings to load values from our .env file.
    # extra="ignore" allows the .env file to contain settings that
    # are not defined in this Settings class.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

# Create one Settings instance that can be imported throughout the application.
settings = Settings()