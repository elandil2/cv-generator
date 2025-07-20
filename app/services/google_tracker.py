import os
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False

def get_env_var(key):
    """Get environment variable from Streamlit secrets or OS env"""
    if STREAMLIT_AVAILABLE:
        try:
            return st.secrets.get(key) or os.getenv(key)
        except:
            return os.getenv(key)
    return os.getenv(key)

class SilentGoogleTracker:
    def __init__(self):
        self.enabled = False
        self.sheets_service = None
        self.spreadsheet_id = get_env_var('GOOGLE_SPREADSHEET_ID')
        
        self._initialize_silently()
    
    def _initialize_silently(self):
        """Initialize Google services silently"""
        try:
            json_str = get_env_var('GOOGLE_SERVICE_ACCOUNT_JSON')
            if json_str:
                service_account_info = json.loads(json_str)
                credentials = Credentials.from_service_account_info(
                    service_account_info,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                
                self.sheets_service = gspread.authorize(credentials)
                self.enabled = True
                
        except Exception as e:
            # Silent failure
            pass
# Global instance
silent_tracker = SilentGoogleTracker()