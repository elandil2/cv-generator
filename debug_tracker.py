import os
from dotenv import load_dotenv

load_dotenv()

print("=== Environment Check ===")
print(f"GOOGLE_SERVICE_ACCOUNT_JSON exists: {bool(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))}")
print(f"GOOGLE_SPREADSHEET_ID: {os.getenv('GOOGLE_SPREADSHEET_ID')}")
print(f"GOOGLE_DRIVE_FOLDER_ID: {os.getenv('GOOGLE_DRIVE_FOLDER_ID')}")

print("\n=== Tracker Check ===")
try:
    from app.services.google_tracker import silent_tracker
    print(f"Tracker enabled: {silent_tracker.enabled}")
    print(f"Sheets service: {bool(silent_tracker.sheets_service)}")
    print(f"Drive service: {bool(silent_tracker.drive_service)}")
    print(f"Spreadsheet ID: {silent_tracker.spreadsheet_id}")
    print(f"Folder ID: {silent_tracker.folder_id}")
    
except Exception as e:
    print(f"Error: {e}")