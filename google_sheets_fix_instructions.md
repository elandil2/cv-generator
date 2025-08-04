# Google Sheets Integration Fixes

## Authentication Simplification
```python
# In app/services/google_tracker.py
def _initialize_silently(self):
    try:
        creds = Credentials.from_service_account_file(
            'service-account.json',
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        self.sheets_service = gspread.authorize(creds)
        self.enabled = True
    except Exception as e:
        st.error(f"Google Sheets auth failed: {str(e)}")
```

## Dockerfile Update
```dockerfile
# Add this to Dockerfile
COPY service-account.json /app/service-account.json
```

## Retry Logic
```python
# Add to API calls in google_tracker.py
import time
retries = 0
while retries < 3:
    try:
        # API call here
        break
    except gspread.exceptions.APIError:
        time.sleep(2)
        retries += 1
```

## Service Account Setup
1. Create service account in Google Cloud Console
2. Download JSON credentials as `service-account.json`
3. Share target spreadsheet with service account email