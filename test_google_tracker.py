import os
from dotenv import load_dotenv

load_dotenv()

print("Testing Google Tracker...")

try:
    from app.services.google_tracker import SilentGoogleTracker
    
    tracker = SilentGoogleTracker()
    print(f"Tracker enabled: {tracker.enabled}")
    
    if tracker.enabled:
        print("✅ Google services initialized successfully!")
    else:
        print("❌ Google services failed to initialize")
        
except Exception as e:
    print(f"❌ Error importing/creating tracker: {e}")
    
    # Try manual initialization
    print("\nTrying manual initialization...")
    try:
        import json
        from google.oauth2.service_account import Credentials
        import gspread
        
        json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        service_account_info = json.loads(json_str)
        
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
        )
        
        sheets_service = gspread.authorize(credentials)
        print("✅ Manual Google Sheets connection successful!")
        
    except Exception as manual_error:
        print(f"❌ Manual initialization failed: {manual_error}")