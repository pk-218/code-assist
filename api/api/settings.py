import os
from pydantic import BaseSettings

import openai

class Settings(BaseSettings):
    path: str = os.getcwd() + "/.env"
    key: str = os.getenv("OPENAI_API_KEY")
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.4
    max_tokens: int = 250
    openai.api_key = key


settings = Settings()
