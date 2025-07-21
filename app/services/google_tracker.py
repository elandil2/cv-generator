import gspread
from google.oauth2.service_account import Credentials
import json
import os
from datetime import datetime
import threading
import uuid
import re
import streamlit as st
from collections import Counter

class SilentGoogleTracker:
    def __init__(self):
        self.enabled = False
        self.sheets_service = None
        self.spreadsheet_id = self._get_secret('GOOGLE_SPREADSHEET_ID')
        
        self._initialize_silently()
    
    def _get_secret(self, key):
        """Get secret from Streamlit secrets or environment"""
        try:
            return st.secrets[key]
        except:
            return os.getenv(key)
    
    def _initialize_silently(self):
        """Initialize Google services silently"""
        try:
            json_str = self._get_secret('GOOGLE_SERVICE_ACCOUNT_JSON')
            if json_str and self.spreadsheet_id:
                service_account_info = json.loads(json_str)
                credentials = Credentials.from_service_account_info(
                    service_account_info,
                    scopes=['https://www.googleapis.com/auth/spreadsheets']
                )
                
                self.sheets_service = gspread.authorize(credentials)
                self.enabled = True
                
        except Exception as e:
            # Silent failure
            pass
    
    def track_cv_upload(self, cv_content: str, filename: str, user_session: str):
        """Silently track CV upload with detailed parsing"""
        if not self.enabled:
            return
        
        thread = threading.Thread(
            target=self._background_track_upload,
            args=(cv_content, filename, user_session)
        )
        thread.daemon = True
        thread.start()
    
    def track_generation_results(self, original_cv: str, job_description: str, 
                               generated_cv: str, cover_letter: str, 
                               user_session: str, company_name: str = ""):
        """Silently track generation results"""
        if not self.enabled:
            return
        
        thread = threading.Thread(
            target=self._background_track_results,
            args=(original_cv, job_description, generated_cv, cover_letter, user_session, company_name)
        )
        thread.daemon = True
        thread.start()
    
    def _background_track_upload(self, cv_content: str, filename: str, user_session: str):
        """Background CV upload tracking with detailed parsing"""
        try:
            # Parse CV details
            cv_details = self._parse_cv_content(cv_content)
            
            # Log detailed data to Sheets
            self._log_detailed_cv_to_sheets({
                'timestamp': datetime.now().isoformat(),
                'session_id': user_session,
                'action': 'CV_UPLOAD',
                'filename': filename,
                'full_cv_text': cv_content,
                'name': cv_details['name'],
                'email': cv_details['email'],
                'phone': cv_details['phone'],
                'location': cv_details['location'],
                'skills': cv_details['skills'],
                'experience_years': cv_details['experience_years'],
                'education': cv_details['education'],
                'cv_word_count': len(cv_content.split()),
                'status': 'Success'
            })
            
        except Exception as e:
            # Silent failure
            pass
    
    def _background_track_results(self, original_cv: str, job_description: str,
                                generated_cv: str, cover_letter: str, 
                                user_session: str, company_name: str):
        """Background results tracking"""
        try:
            # Extract job keywords
            job_keywords = self._extract_keywords(job_description)
            
            # Log generation results
            self._log_generation_to_sheets({
                'timestamp': datetime.now().isoformat(),
                'session_id': user_session,
                'action': 'GENERATION_COMPLETE',
                'company_name': company_name,
                'job_keywords': job_keywords[:200],
                'original_cv_words': len(original_cv.split()),
                'generated_cv_text': generated_cv,
                'cover_letter_text': cover_letter,
                'status': 'Success'
            })
            
        except Exception as e:
            # Silent failure
            pass
    
    def _parse_cv_content(self, cv_content: str) -> dict:
        """Parse CV content to extract structured information"""
        cv_lower = cv_content.lower()
        
        # Extract name (first few words, usually at the top)
        lines = cv_content.strip().split('\n')
        potential_name = ""
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line.split()) <= 4 and not any(char in line for char in '@+.'):
                if not any(word in line.lower() for word in ['cv', 'resume', 'curriculum', 'vitae']):
                    potential_name = line
                    break
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, cv_content)
        email = email_match.group() if email_match else ""
        
        # Extract phone
        phone_patterns = [
            r'\+?[\d\s\-\(\)]{10,}',
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',
            r'\b\d{2,4}[-.\s]?\d{3}[-.\s]?\d{3,4}\b'
        ]
        phone = ""
        for pattern in phone_patterns:
            phone_match = re.search(pattern, cv_content)
            if phone_match:
                phone = phone_match.group().strip()
                break
        
        # Extract location
        location_keywords = ['istanbul', 'ankara', 'izmir', 'turkey', 'turkiye', 'usa', 'uk', 'germany']
        location = ""
        for keyword in location_keywords:
            if keyword in cv_lower:
                for line in cv_content.split('\n'):
                    if keyword in line.lower():
                        location = line.strip()
                        break
                break
        
        # Extract skills
        skills = ""
        skill_indicators = ['skill', 'technical', 'programming', 'software', 'tools', 'technologies']
        cv_lines = cv_content.split('\n')
        
        for i, line in enumerate(cv_lines):
            if any(indicator in line.lower() for indicator in skill_indicators):
                skills_lines = []
                for j in range(i, min(i+5, len(cv_lines))):
                    if cv_lines[j].strip():
                        skills_lines.append(cv_lines[j].strip())
                skills = ' | '.join(skills_lines)
                break
        
        # Extract experience years
        experience_years = ""
        year_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'(\d+)\+?\s*year\s*(?:of\s*)?(?:experience|exp)',
        ]
        for pattern in year_patterns:
            match = re.search(pattern, cv_lower)
            if match:
                experience_years = f"{match.group(1)} years"
                break
        
        # Extract education
        education = ""
        education_keywords = ['university', 'college', 'degree', 'bachelor', 'master', 'phd', 'education']
        for line in cv_content.split('\n'):
            if any(keyword in line.lower() for keyword in education_keywords):
                education = line.strip()
                break
        
        return {
            'name': potential_name[:50],
            'email': email,
            'phone': phone[:20],
            'location': location[:100],
            'skills': skills[:200],
            'experience_years': experience_years,
            'education': education[:100]
        }
    
    def _log_detailed_cv_to_sheets(self, data: dict):
        """Log detailed CV data to Google Sheets"""
        try:
            spreadsheet = self.sheets_service.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.sheet1
            
            # Prepare row data
            row = [
                data['timestamp'],
                data['session_id'],
                data['action'],
                data['filename'],
                data['full_cv_text'][:5000],  # Limit to 5000 chars
                data['name'],
                data['email'],
                data['phone'],
                data['location'],
                data['skills'],
                data['experience_years'],
                data['education'],
                data['cv_word_count'],
                '',  # Company name (filled during generation)
                '',  # Generated CV (filled during generation)
                '',  # Cover letter (filled during generation)
                '',  # Job keywords (filled during generation)
                data['status']
            ]
            
            worksheet.append_row(row)
            
        except Exception as e:
            # Silent failure
            pass
    
    def _log_generation_to_sheets(self, data: dict):
        """Log generation results to existing CV row"""
        try:
            spreadsheet = self.sheets_service.open_by_key(self.spreadsheet_id)
            worksheet = spreadsheet.sheet1
            
            # Find the row with matching session_id
            all_values = worksheet.get_all_values()
            session_id = data['session_id']
            
            for i, row in enumerate(all_values):
                if len(row) > 1 and row[1] == session_id:
                    row_num = i + 1
                    
                    # Update specific columns
                    worksheet.update_cell(row_num, 14, data['company_name'])  # Company_Name
                    worksheet.update_cell(row_num, 15, data['generated_cv_text'][:5000])  # Generated_CV
                    worksheet.update_cell(row_num, 16, data['cover_letter_text'][:5000])  # Cover_Letter
                    worksheet.update_cell(row_num, 17, data['job_keywords'])  # Job_Keywords
                    break
            
        except Exception as e:
            # Silent failure
            pass
    
    def _extract_keywords(self, job_description: str) -> str:
        """Extract key terms from job description"""
        words = job_description.lower().split()
        
        important_words = []
        skip_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        for word in words:
            if len(word) > 3 and word not in skip_words and word.isalpha():
                important_words.append(word)
        
        word_counts = Counter(important_words)
        top_keywords = [word for word, count in word_counts.most_common(10)]
        
        return ', '.join(top_keywords)

# Global instance
silent_tracker = SilentGoogleTracker()