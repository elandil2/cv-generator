from .llm_service import LLMService
from typing import Dict, Any

class CVGenerator:
    def __init__(self):
        self.llm_service = LLMService()
    
    def generate_tailored_cv(self, original_cv: str, job_description: str, user_preferences: Dict[str, Any] = None) -> str:
        system_prompt = """
        You are an expert CV writer. Your task is to create a highly optimized CV that maximizes keyword matching.

        CRITICAL REQUIREMENTS:
        1. NEVER remove any work experience - keep ALL jobs but reorder by relevance
        2. USE EXACT technical terms and keywords from the job description
        3. QUANTIFY achievements with realistic numbers (not placeholders like [X]%)
        4. ADD missing technical skills that match the role
        5. OPTIMIZE for 80%+ keyword matching with job description
        6. Keep the same contact information and basic structure
        7. Make it ATS-friendly with clear sections

        STRATEGY:
        - Put most relevant experience first
        - Integrate job description keywords naturally
        - Enhance technical skills section with job requirements
        - Strengthen achievements with specific metrics
        - Maintain professional formatting
        """
        
        user_prompt = f"""
        ORIGINAL CV:
        {original_cv}

        TARGET JOB DESCRIPTION:
        {job_description}

        TASK: Create a CV with 80%+ keyword match. 

        REQUIREMENTS:
        1. Keep ALL work experience but reorder by relevance to job
        2. Extract and use these technical keywords from job description naturally
        3. Replace vague achievements with specific numbers
        4. Add missing skills mentioned in job posting to skills section
        5. Optimize each section for maximum keyword density

        Focus Areas: {user_preferences.get('focus_areas', []) if user_preferences else ['Technical Skills', 'Achievements']}

        OUTPUT: Complete, keyword-optimized CV that will score 80%+ match with the job description.
        """
        
        response = self.llm_service.generate_response(system_prompt, user_prompt)
        return response