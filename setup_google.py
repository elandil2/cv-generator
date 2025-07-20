import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup():
    try:
        from app.services.google_tracker import SilentGoogleTracker
        
        tracker = SilentGoogleTracker()
        
        if tracker.enabled:
            print("✅ Google services connected!")
            
            # Create spreadsheet
            print("Creating spreadsheet...")
            spreadsheet = tracker.sheets_service.create("CV Generator Tracking")
            worksheet = spreadsheet.sheet1
            
            # Add headers
            headers = [
                'Timestamp', 'Session_ID', 'Action', 'Company/Filename', 
                'CV_Word_Count', 'Original_CV_Link', 'Generated_CV_Link', 
                'Cover_Letter_Link', 'Job_Keywords', 'Reserved', 'Status'
            ]
            worksheet.append_row(headers)
            
            # Make spreadsheet public (anyone with link can edit)
            spreadsheet.share('', perm_type='anyone', role='writer')
            
            print(f"✅ Spreadsheet created!")
            print(f"URL: {spreadsheet.url}")
            print(f"GOOGLE_SPREADSHEET_ID={spreadsheet.id}")
            
            # Create drive folder
            print("Creating drive folder...")
            folder_metadata = {
                'name': 'CV Generator Uploads',
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = tracker.drive_service.files().create(
                body=folder_metadata, 
                fields='id,webViewLink'
            ).execute()
            
            # Make folder public
            permission = {
                'type': 'anyone',
                'role': 'writer'
            }
            tracker.drive_service.permissions().create(
                fileId=folder.get('id'), 
                body=permission
            ).execute()
            
            print(f"✅ Drive folder created!")
            print(f"GOOGLE_DRIVE_FOLDER_ID={folder.get('id')}")
            
            print("\n📝 Add these to your .env file:")
            print(f"GOOGLE_SPREADSHEET_ID={spreadsheet.id}")
            print(f"GOOGLE_DRIVE_FOLDER_ID={folder.get('id')}")
            
        else:
            print("❌ Google services not enabled")
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup()