# test_env.py
import os
from dotenv import load_dotenv

load_dotenv()

print("GOOGLE_DRIVE_FOLDER_ID:", repr(os.getenv('GOOGLE_DRIVE_FOLDER_ID')))
print("GOOGLE_SPREADSHEET_ID:", repr(os.getenv('GOOGLE_SPREADSHEET_ID')))