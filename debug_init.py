# debug_init.py
import os
from dotenv import load_dotenv
import json

load_dotenv()

print("=== Step by Step Debug ===")

# Check environment
json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
spreadsheet_id = os.getenv('GOOGLE_SPREADSHEET_ID')
folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

print(f"1. JSON exists: {bool(json_str)}")
print(f"2. Spreadsheet ID: {spreadsheet_id}")
print(f"3. Folder ID: {folder_id}")

# Test JSON parsing
if json_str:
    try:
        service_account_info = json.loads(json_str)
        print("4. JSON parsing: ✅ Success")
    except Exception as e:
        print(f"4. JSON parsing: ❌ Failed - {e}")

# Test Google imports
try:
    from google.oauth2.service_account import Credentials
    import gspread
    from googleapiclient.discovery import build
    print("5. Google imports: ✅ Success")
except Exception as e:
    print(f"5. Google imports: ❌ Failed - {e}")

# Test credentials creation
try:
    if json_str:
        service_account_info = json.loads(json_str)
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.file'
            ]
        )
        print("6. Credentials creation: ✅ Success")
        
        # Test services
        sheets_service = gspread.authorize(credentials)
        drive_service = build('drive', 'v3', credentials=credentials)
        print("7. Services creation: ✅ Success")
        
    except Exception as e:
        print(f"6-7. Service creation: ❌ Failed - {e}")
        import traceback
        traceback.print_exc()

print("\n=== Now test tracker ===")
from app.services.google_tracker import SilentGoogleTracker
tracker = SilentGoogleTracker()
print(f"Final result - Tracker enabled: {tracker.enabled}")