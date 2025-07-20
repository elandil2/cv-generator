# direct_drive_test.py
import os
import json
import io
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

load_dotenv()

def direct_drive_test():
    try:
        # Get credentials
        json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
        folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
        
        service_account_info = json.loads(json_str)
        credentials = Credentials.from_service_account_info(
            service_account_info,
            scopes=['https://www.googleapis.com/auth/drive.file']
        )
        
        # Create drive service
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # Test upload
        test_content = "This is a test CV upload - direct method"
        file_metadata = {
            'name': 'direct_test.txt',
            'parents': [folder_id]
        }
        
        content_io = io.BytesIO(test_content.encode('utf-8'))
        media = MediaIoBaseUpload(content_io, mimetype='text/plain')
        
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id,webViewLink'
        ).execute()
        
        # Make public
        permission = {'type': 'anyone', 'role': 'reader'}
        drive_service.permissions().create(fileId=file.get('id'), body=permission).execute()
        
        print(f"✅ SUCCESS! File uploaded!")
        print(f"Link: {file.get('webViewLink')}")
        print("Check your Google Drive folder!")
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    direct_drive_test()