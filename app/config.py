import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    # Add other settings here, e.g., SECRET_KEY


settings = Settings()
