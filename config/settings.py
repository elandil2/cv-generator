import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        self.app_name = "CV & Cover Letter Generator"
        self.version = "1.0.0"
        self.debug = False
        self.max_file_size = 5 * 1024 * 1024  # 5MB

settings = Settings()