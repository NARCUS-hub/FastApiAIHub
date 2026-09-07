import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    gemini_api_key = os.getenv("GEMINI_API_KEY", "")


config_obj = Config()
