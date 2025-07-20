from typing import Dict, List

class CVTemplate:
    @staticmethod
    def format_professional_cv(cv_data: Dict) -> str:
        """Format CV data into a professional template"""
        
        template = """
{header}

PROFESSIONAL SUMMARY
{professional_summary}

KEY SKILLS
{key_skills}

WORK EXPERIENCE
{work_experience}

EDUCATION
{education}

{additional_sections}
        """.strip()
        
        # Format header
        header = cv_data.get('contact_info', '[Your Name]\n[Your Email] | [Your Phone]\n[Your Address]')
        
        # Format professional summary
        professional_summary = cv_data.get('professional_summary', '')
        
        # Format key skills
        skills = cv_data.get('key_skills', [])
        if isinstance(skills, list):
            key_skills = ' • '.join(skills)
        else:
            key_skills = skills
        
        # Format work experience
        work_exp = cv_data.get('work_experience', [])
        work_experience = ""
        if isinstance(work_exp, list):
            for exp in work_exp:
                if isinstance(exp, dict):
                    work_experience += f"""
{exp.get('role', '')} | {exp.get('company', '')}
{exp.get('duration', '')}
{exp.get('achievements', '')}

"""
                else:
                    work_experience += f"{exp}\n\n"
        else:
            work_experience = work_exp
        
        # Format education
        education = cv_data.get('education', '')
        
        # Format additional sections
        additional = cv_data.get('additional_sections', '')
        
        return template.format(
            header=header,
            professional_summary=professional_summary,
            key_skills=key_skills,
            work_experience=work_experience.strip(),
            education=education,
            additional_sections=additional
        )
    
    @staticmethod
    def format_modern_cv(cv_data: Dict) -> str:
        """Format CV data into a modern template"""
        
        template = """
═══════════════════════════════════════════════════════════════
{header}
═══════════════════════════════════════════════════════════════

🎯 PROFESSIONAL SUMMARY
{professional_summary}

💼 CORE COMPETENCIES
{key_skills}

🚀 PROFESSIONAL EXPERIENCE
{work_experience}

🎓 EDUCATION & QUALIFICATIONS
{education}

{additional_sections}
        """.strip()
        
        return CVTemplate._populate_template(template, cv_data)
    
    @staticmethod
    def _populate_template(template: str, cv_data: Dict) -> str:
        """Helper method to populate template with data"""
        # Similar logic as format_professional_cv but with different styling
        return template  # Implementation would be similar to above

class CoverLetterTemplate:
    @staticmethod
    def format_professional_cover_letter(
        content: str,
        company_name: str = "[Company Name]",
        hiring_manager: str = "Hiring Manager",
        applicant_name: str = "[Your Name]"
    ) -> str:
        """Format cover letter with professional template"""
        
        template = f"""
{applicant_name}
[Your Address]
[City, State ZIP Code]
[Your Email]
[Your Phone Number]

[Date]

{hiring_manager}
{company_name}
[Company Address]

Dear {hiring_manager},

{content}

Sincerely,
{applicant_name}
        """.strip()
        
        return template
    
    @staticmethod
    def format_modern_cover_letter(
        content: str,
        company_name: str = "[Company Name]",
        hiring_manager: str = "Hiring Manager",
        applicant_name: str = "[Your Name]"
    ) -> str:
        """Format cover letter with modern template"""
        
        template = f"""
═══════════════════════════════════════════════════════════════

{applicant_name} | [Your Email] | [Your Phone] | [Your LinkedIn]

═══════════════════════════════════════════════════════════════

{hiring_manager}
{company_name}

Subject: Application for [Position Title] - {applicant_name}

{content}

Best regards,
{applicant_name}

═══════════════════════════════════════════════════════════════
        """.strip()
        
        return template