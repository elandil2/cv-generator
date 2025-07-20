# debug_tracker_detailed.py
import os
from dotenv import load_dotenv

load_dotenv()

print("=== Testing Tracker Initialization ===")

try:
    from app.services.google_tracker import SilentGoogleTracker
    
    # Create new instance to debug
    tracker = SilentGoogleTracker()
    
    print(f"Tracker enabled: {tracker.enabled}")
    print(f"Spreadsheet ID: {tracker.spreadsheet_id}")
    print(f"Folder ID: {tracker.folder_id}")
    print(f"Sheets service exists: {tracker.sheets_service is not None}")
    print(f"Drive service exists: {tracker.drive_service is not None}")
    
    # Test the logic
    has_json = bool(os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON'))
    has_spreadsheet = bool(tracker.spreadsheet_id)
    has_folder = bool(tracker.folder_id)
    
    print(f"\nLogic check:")
    print(f"Has JSON: {has_json}")
    print(f"Has Spreadsheet ID: {has_spreadsheet}")
    print(f"Has Folder ID: {has_folder}")
    print(f"Should be enabled: {has_json and has_spreadsheet and has_folder}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()