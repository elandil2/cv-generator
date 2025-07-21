import groq
from config.settings import settings
import logging

class LLMService:
    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq client without any extra parameters
        self.client = groq.Groq(api_key=settings.groq_api_key)
        self.model = "llama3-8b-8192"
    
    def generate_response(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate content: {str(e)}")