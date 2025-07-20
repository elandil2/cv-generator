from .llm_service import LLMService
from typing import Dict, Any

class CoverLetterGenerator:
    def __init__(self):
        self.llm_service = LLMService()
    
    def generate_cover_letter(
        self, 
        cv_content: str, 
        job_description: str, 
        company_info: Dict[str, str] = None,
        user_details: Dict[str, str] = None,
        tone: str = "professional"
    ) -> str:
        
        company_name = company_info.get("name", "[Company Name]") if company_info else "[Company Name]"
        hiring_manager = company_info.get("hiring_manager", "Hiring Manager") if company_info else "Hiring Manager"
        
        system_prompt = f"""
        You are an expert cover letter writer. Create a compelling, personalized cover letter that:
        
        1. Opens with a strong hook that shows genuine interest
        2. Demonstrates clear understanding of the role and company
        3. Highlights 2-3 most relevant achievements from the CV
        4. Shows cultural fit and enthusiasm
        5. Includes a clear call to action
        6. Maintains a {tone} tone throughout
        7. Is concise (3-4 paragraphs, ~300-400 words)
        8. Avoids generic phrases and clichés
        
        Structure:
        - Professional header with contact information
        - Date and company details
        - Engaging opening paragraph
        - 1-2 body paragraphs with specific examples
        - Strong closing paragraph
        - Professional signature
        """
        
        user_prompt = f"""
        CV Content:
        {cv_content}
        
        Job Description:
        {job_description}
        
        Company: {company_name}
        Hiring Manager: {hiring_manager}
        
        Create a tailored cover letter that makes this candidate stand out for this specific role.
        """
        
        return self.llm_service.generate_response(system_prompt, user_prompt)