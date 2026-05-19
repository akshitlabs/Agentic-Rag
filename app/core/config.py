from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Ye teeno naam aapki .env file se match ho rahe hain
    database_url: str
    redis_url: str
    secret_key: str

    # Pydantic ko bata rahe hain ki data .env se padhna hai
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Is 'settings' variable ko hum pure project me use karenge
settings = Settings()
