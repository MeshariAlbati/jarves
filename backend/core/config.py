from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    anthropic_api_key: str
    groq_api_key: str
    langsmith_api_key: str
    langsmith_project: str
    langsmith_tracing: str
    telegram_bot_token: str
    supabase_url: str
    supabase_key: str
    telegram_chat_id: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
