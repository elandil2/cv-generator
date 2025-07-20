import re
from typing import Dict, List, Optional

class Validators:
    @staticmethod
    def validate_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        # Basic phone validation - can be enhanced
        pattern = r'^[\+]?[1-9][\d]{0,15}$'
        cleaned_phone = re.sub(r'[\s\-\(\)]', '', phone)
        return len(cleaned_phone) >= 7 and re.match(pattern, cleaned_phone) is not None
    
    @staticmethod
    def validate_required_fields(data: Dict[str, str], required_fields: List[str]) -> List[str]:
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field].strip():
                missing_fields.append(field)
        return missing_fields
    
    @staticmethod
    def validate_cv_content(cv_text: str) -> Dict[str, bool]:
        """Validate if CV contains essential sections"""
        cv_lower = cv_text.lower()
        
        validations = {
            "has_contact_info": any(keyword in cv_lower for keyword in ['email', '@', 'phone', 'contact']),
            "has_experience": any(keyword in cv_lower for keyword in ['experience', 'work', 'employment', 'job']),
            "has_skills": any(keyword in cv_lower for keyword in ['skill', 'technical', 'competenc']),
            "has_education": any(keyword in cv_lower for keyword in ['education', 'degree', 'university', 'college']),
            "sufficient_length": len(cv_text.split()) > 100
        }
        
        return validations