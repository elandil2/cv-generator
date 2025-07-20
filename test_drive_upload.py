from app.services.google_tracker import SilentGoogleTracker

def test_drive():
    # Create new instance instead of using global
    tracker = SilentGoogleTracker()
    
    if tracker.enabled:
        print("Testing Drive upload...")
        
        test_content = "This is a test CV content for upload"
        result = tracker._upload_to_drive(test_content, "test_cv_upload")
        
        if result:
            print(f"✅ Drive upload works! Link: {result}")
            print("Check your Google Drive folder!")
        else:
            print("❌ Drive upload failed")
    else:
        print("❌ Tracker not enabled")

if __name__ == "__main__":
    test_drive()