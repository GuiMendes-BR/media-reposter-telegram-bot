import os

# from pydantic_settings import BaseSettings
from pydantic import Field, DirectoryPath, AnyUrl, BaseSettings


class Settings(BaseSettings):
    """This class contains settings for the project
    """
    process_id: str = Field(..., env="PROCESS_ID")

    # Telegram Api Credentials
    telegram_api_id: str = Field(..., env="TELEGRAM_API_ID")
    telegram_api_hash: str = Field(..., env="TELEGRAM_API_HASH")
    telegram_api_bot_token: str = Field(..., env="TELEGRAM_API_BOT_TOKEN")

    # Instagram Credentials
    instagram_username: str = Field(..., env="INSTAGRAM_USERNAME")
    instagram_password: str = Field(..., env="INSTAGRAM_PASSWORD")

    # URLs
    instagram_url: AnyUrl = Field(..., env="INSTAGRAM_URL")
    sssinstagram_url: AnyUrl = Field(..., env="SSSINSTAGRAM_URL")
    
    # Proxy
    use_proxy: bool = Field(..., env="USE_PROXY")
    proxy: str = Field(..., env="proxy")
    
    # Folders
    downloads_folder: DirectoryPath = Field(..., env="DOWNLOADS_FOLDER")
    logs_folder: DirectoryPath = Field(..., env="LOGS_FOLDER")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()
