import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self):
        # Try Streamlit secrets first, then fall back to environment variables
        try:
            self.groq_api_key = st.secrets["GROQ_API_KEY"]
        except (KeyError, AttributeError):
            self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        
        self.app_name = "CV & Cover Letter Generator"
        self.version = "1.0.0"
        self.debug = False
        self.max_file_size = 5 * 1024 * 1024

settings = Settings()