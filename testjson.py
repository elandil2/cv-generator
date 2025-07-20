import os
from dotenv import load_dotenv
import json

load_dotenv()

json_str = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON')
print(f"JSON exists: {bool(json_str)}")

if json_str:
    try:
        json_data = json.loads(json_str)
        print(f"JSON valid: True")
        print(f"Project ID: {json_data.get('project_id')}")
        print(f"Client email: {json_data.get('client_email')}")
    except Exception as e:
        print(f"JSON invalid: {e}")
else:
    print("No JSON found in environment")