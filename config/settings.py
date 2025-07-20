import os
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

from dotenv import load_dotenv
load_dotenv()

def get_env_var(key, default=""):
    """Get environment variable from Streamlit secrets or OS env"""
    if STREAMLIT_AVAILABLE:
        try:
            return st.secrets.get(key, default) or os.getenv(key, default)
        except:
            return os.getenv(key, default)
    return os.getenv(key, default)

class Settings:
    def __init__(self):
        self.groq_api_key = get_env_var("GROQ_API_KEY")
        self.app_name = "CV & Cover Letter Generator"
        self.version = "1.0.0"
        self.debug = False
        self.max_file_size = 5 * 1024 * 1024

settings = Settings()