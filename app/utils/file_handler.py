import PyPDF2
from docx import Document
import streamlit as st
from typing import Optional
import tempfile
import os

class FileHandler:
    @staticmethod
    def extract_text_from_pdf(file) -> str:
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_docx(file) -> str:
        try:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    @staticmethod
    def extract_text_from_file(uploaded_file) -> Optional[str]:
        if uploaded_file is None:
            return None
        
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return FileHandler.extract_text_from_pdf(uploaded_file)
        elif file_extension in ['docx', 'doc']:
            return FileHandler.extract_text_from_docx(uploaded_file)
        elif file_extension == 'txt':
            return str(uploaded_file.read(), "utf-8")
        else:
            st.error("Unsupported file format. Please upload PDF, DOCX, or TXT files.")
            return None
    
    @staticmethod
    def save_temp_file(content: str, filename: str, format_type: str = "txt") -> str:
        """Save content to temporary file and return path"""
        try:
            temp_dir = "data/uploads"
            os.makedirs(temp_dir, exist_ok=True)
            
            file_path = os.path.join(temp_dir, f"{filename}.{format_type}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return file_path
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")
            return None