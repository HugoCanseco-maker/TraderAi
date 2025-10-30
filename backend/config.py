import os


class Settings:
    twelve_data_api_key: str = os.getenv("TWELVE_DATA_API_KEY", "")
    frontend_url: str | None = os.getenv("FRONTEND_URL")


settings = Settings()


