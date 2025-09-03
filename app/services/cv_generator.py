from .llm_service import LLMService
from typing import Dict, Any

class CVGenerator:
    def __init__(self):
        self.llm_service = LLMService()

    # Role-specific system prompts for better agent context
    ROLE_PROMPTS = {
        "general": """
        You are an expert CV writer. Your task is to create a highly optimized CV that maximizes keyword matching.
        """,
        "data_scientist": """
        You are a senior data science recruiter and CV optimization expert specializing in data science roles.
        Focus on: statistical modeling, machine learning algorithms, data visualization, Python/R proficiency,
        big data tools (Spark, Hadoop), cloud platforms (AWS, GCP, Azure), SQL/NoSQL databases.
        Prioritize: predictive modeling experience, A/B testing, feature engineering, data pipeline development.
        """,
        "ml_engineer": """
        You are an ML engineering specialist focusing on production machine learning systems.
        Focus on: model deployment, MLOps, containerization (Docker, Kubernetes), CI/CD pipelines,
        model monitoring, scalable inference, API development, performance optimization.
        Prioritize: production ML systems, automated pipelines, model versioning, A/B testing frameworks.
        """,
        "genai_engineer": """
        You are a Generative AI expert specializing in large language models and AI systems.
        Focus on: LLM fine-tuning, prompt engineering, RAG systems, multimodal models,
        transformer architectures, ethical AI considerations, model deployment at scale.
        Prioritize: custom model training, inference optimization, safety alignment, prompt optimization.
        """,
        "software_engineer": """
        You are a software engineering expert focusing on full-stack development and system design.
        Focus on: programming languages (Python, Java, JavaScript), frameworks, databases,
        cloud services, microservices, API design, testing methodologies.
        Prioritize: system architecture, scalable solutions, code quality, DevOps practices.
        """,
        "devops_engineer": """
        You are a DevOps engineering specialist focusing on infrastructure and deployment.
        Focus on: cloud platforms (AWS, GCP, Azure), containerization (Docker, Kubernetes),
        CI/CD pipelines, infrastructure as code (Terraform), monitoring tools, security practices.
        Prioritize: automation, scalability, reliability, cost optimization, security compliance.
        """
    }

    def generate_tailored_cv(self, original_cv: str, job_description: str, job_type: str = "general", user_preferences: Dict[str, Any] = None) -> str:
        # Get role-specific base prompt
        base_prompt = self.ROLE_PROMPTS.get(job_type, self.ROLE_PROMPTS["general"])

        system_prompt = f"""
        {base_prompt}

        CRITICAL REQUIREMENTS:
        1. NEVER remove any work experience - keep ALL jobs but reorder by relevance
        2. USE EXACT technical terms and keywords from the job description
        3. QUANTIFY achievements with realistic numbers (not placeholders like [X]%)
        4. ADD missing technical skills that match the {job_type.replace('_', ' ')} role
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