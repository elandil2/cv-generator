import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from services.cv_generator import CVGenerator
from services.cover_letter_generator import CoverLetterGenerator
from utils.validators import Validators

class TestCVGenerator(unittest.TestCase):
    def setUp(self):
        self.cv_generator = CVGenerator()
    
    @patch('services.cv_generator.LLMService')
    def test_generate_tailored_cv(self, mock_llm_service):
        # Mock the LLM response
        mock_llm_service.return_value.generate_response.return_value = '{"professional_summary": "Test summary"}'
        
        result = self.cv_generator.generate_tailored_cv(
            "Test CV content",
            "Test job description"
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("professional_summary", result)

class TestValidators(unittest.TestCase):
    def test_validate_email(self):
        self.assertTrue(Validators.validate_email("test@example.com"))
        self.assertFalse(Validators.validate_email("invalid-email"))
    
    def test_validate_cv_content(self):
        cv_text = "John Doe\nSoftware Engineer\nEmail: john@example.com\nExperience in Python\nEducation: BS Computer Science"
        validations = Validators.validate_cv_content(cv_text)
        
        self.assertTrue(validations["has_contact_info"])
        self.assertTrue(validations["has_experience"])
        self.assertTrue(validations["has_education"])

if __name__ == '__main__':
    unittest.main()