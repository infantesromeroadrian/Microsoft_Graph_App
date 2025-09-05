"""
Configuration settings for the Microsoft Graph webhook receiver
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    app_name: str = "Microsoft Graph Webhook Receiver"
    app_version: str = "1.0.0"
    api_prefix: str = "/api"

    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # Microsoft Graph Configuration
    graph_api_url: str = "https://graph.microsoft.com/v1.0"
    tenant_id: str | None = None
    client_id: str | None = None
    client_secret: str | None = None
    access_token: str | None = None

    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Payment Notification Configuration
    payment_notification_recipient: str | None = None

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields in .env file


# Create global settings instance
settings = Settings()
