import os
from pydantic import BaseSettings

import openai
import dotenv


class Settings(BaseSettings):
    path: str = os.getcwd() + "/.env"
    key: str = dotenv.get_key(path, "OPENAI_SECRET_KEY")
    model: str = "gpt-3.5-turbo"
    temperature: float = 0.4
    max_tokens: int = 250
    openai.api_key = key


settings = Settings()
