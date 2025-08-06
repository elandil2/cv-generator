import streamlit as st
import sys
import os
import uuid

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import settings
from app.services.llm_service import LLMService
from app.services.cv_generator import CVGenerator
from app.services.cover_letter_generator import CoverLetterGenerator
from app.utils.file_handler import FileHandler
from app.utils.analytics import CVAnalytics
from app.services.google_tracker import SilentGoogleTracker

# Create instance in main.py
silent_tracker = SilentGoogleTracker()

# Page configuration
st.set_page_config(
    page_title="AI CV & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #333;
        margin: 1.5rem 0 1rem 0;
        border-bottom: 2px solid #1E88E5;
        padding-bottom: 0.5rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1E88E5;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    if 'cv_content' not in st.session_state:
        st.session_state.cv_content = ""
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'generated_cv' not in st.session_state:
        st.session_state.generated_cv = None
    if 'generated_cover_letter' not in st.session_state:
        st.session_state.generated_cover_letter = None
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]

def main():
    initialize_session_state()
    
    st.markdown('<h1 class="main-header">🤖 AI CV & Cover Letter Generator</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔧 Settings")
        
        # API Key check
        if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
            st.error("⚠️ Groq API key not configured!")
            st.info("Please set your GROQ_API_KEY in the environment variables.")
            return
        else:
            st.success("✅ API configured")
        
        st.markdown("---")
        
        # Generation options
        st.markdown("### 🎯 Generation Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            cv_tone = st.selectbox(
                "CV Tone",
                ["Technical", "Achievement-focused", "Leadership-oriented"],
                help="Choose the tone for your tailored CV"
            )
            
        with col2:
            cover_letter_tone = st.selectbox(
                "Cover Letter Tone",
                ["Professional", "Enthusiastic", "Creative"],
                help="Choose the tone for your cover letter"
            )
        
        cv_focus = st.multiselect(
            "CV Focus Areas",
            ["Technical Skills", "Leadership", "Achievements", "Education", "Certifications"],
            default=["Technical Skills", "Achievements"],
            help="Select areas to emphasize in your tailored CV"
        )
        
        generate_multiple = st.checkbox(
            "Generate Multiple Cover Letter Versions",
            help="Generate cover letters with different tones"
        )
        
        st.markdown("---")
        st.markdown("### 👀 Preview Options")
        preview_mode = st.selectbox(
            "Preview Style",
            ["Full", "Split View", "Diff Comparison"],
            help="Choose how to preview generated documents"
        )
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Upload & Input", "🎯 Generate Documents", "📋 Results", "📊 Analytics"])
    
    with tab1:
        st.markdown('<div class="section-header">Upload Your Current CV</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_cv = st.file_uploader(
                "Choose your CV file",
                type=['pdf', 'docx', 'txt'],
                help="Upload your current CV in PDF, DOCX, or TXT format"
            )
            
            if uploaded_cv:
                with st.spinner("Extracting text from CV..."):
                    cv_text = FileHandler.extract_text_from_file(uploaded_cv)
                    if cv_text:
                        st.session_state.cv_content = cv_text
                        st.success(f"✅ CV uploaded successfully! ({len(cv_text.split())} words)")
                        
                        # Silent tracking - CV upload
                        silent_tracker.track_cv_upload(
                            cv_text, 
                            uploaded_cv.name, 
                            st.session_state.session_id
                        )
                        
                        with st.expander("📊 View CV Content"):
                            st.text_area("CV Content", cv_text, height=200, disabled=True)
        
        with col2:
            st.markdown('<div class="info-box">', unsafe_allow_html=True)
            st.markdown("**💡 Tips for best results:**")
            st.markdown("• Use a well-structured CV")
            st.markdown("• Include contact information")
            st.markdown("• List relevant experience")
            st.markdown("• Mention key skills")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Manual CV input option
        st.markdown("**Or paste your CV content directly:**")
        manual_cv = st.text_area(
            "CV Content",
            value=st.session_state.cv_content,
            height=200,
            placeholder="Paste your CV content here...",
            key="manual_cv_input"
        )
        
        if manual_cv != st.session_state.cv_content:
            st.session_state.cv_content = manual_cv
        
        st.markdown('<div class="section-header">Job Description</div>', unsafe_allow_html=True)
        
        job_desc = st.text_area(
            "Paste the job description you're applying for",
            value=st.session_state.job_description,
            height=300,
            placeholder="Copy and paste the complete job description here...",
            key="job_desc_input"
        )
        
        if job_desc != st.session_state.job_description:
            st.session_state.job_description = job_desc
        
        # Company information (optional)
        with st.expander("🏢 Company Information (Optional)"):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name", key="company_name")
                hiring_manager = st.text_input("Hiring Manager Name", key="hiring_manager")
            with col2:
                company_website = st.text_input("Company Website", key="company_website")
                application_source = st.text_input("Where did you find this job?", key="app_source")
    
    with tab2:
        st.markdown('<div class="section-header">Generate Tailored Documents</div>', unsafe_allow_html=True)
        
        if not st.session_state.cv_content or not st.session_state.job_description:
            st.warning("⚠️ Please provide both CV content and job description in the first tab.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎯 Generate Tailored CV", type="primary", use_container_width=True):
                with st.spinner("Generating tailored CV..."):
                    try:
                        cv_generator = CVGenerator()
                        
                        user_preferences = {
                            "focus_areas": cv_focus,
                            "emphasize_keywords": True
                        }
                        
                        generated_cv = cv_generator.generate_tailored_cv(
                            st.session_state.cv_content,
                            st.session_state.job_description,
                            user_preferences
                        )
                        
                        st.session_state.generated_cv = generated_cv
                        st.success("✅ CV generated successfully!")
                        
                        # Silent tracking - CV generation
                        cover_letter_text = ""
                        if st.session_state.generated_cover_letter:
                            if isinstance(st.session_state.generated_cover_letter, dict):
                                cover_letter_text = str(list(st.session_state.generated_cover_letter.values())[0])
                            else:
                                cover_letter_text = str(st.session_state.generated_cover_letter)
                        
                        silent_tracker.track_generation_results(
                            st.session_state.cv_content,
                            st.session_state.job_description,
                            generated_cv,
                            cover_letter_text,
                            st.session_state.session_id,
                            st.session_state.get("company_name", "")
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error generating CV: {str(e)}")
        
        with col2:
            if st.button("💌 Generate Cover Letter", type="primary", use_container_width=True):
                with st.spinner("Generating cover letter..."):
                    try:
                        cover_letter_generator = CoverLetterGenerator()
                        
                        company_info = {
                            "name": st.session_state.get("company_name", ""),
                            "hiring_manager": st.session_state.get("hiring_manager", ""),
                        }
                        
                        if generate_multiple:
                            generated_letters = {}
                            tones = ["professional", "enthusiastic", "creative"]
                            
                            for tone in tones:
                                letter = cover_letter_generator.generate_cover_letter(
                                    st.session_state.cv_content,
                                    st.session_state.job_description,
                                    company_info,
                                    tone=tone
                                )
                                generated_letters[tone] = letter
                            
                            st.session_state.generated_cover_letter = generated_letters
                        else:
                            generated_letter = cover_letter_generator.generate_cover_letter(
                                st.session_state.cv_content,
                                st.session_state.job_description,
                                company_info,
                                tone=cover_letter_tone.lower()
                            )
                            st.session_state.generated_cover_letter = {cover_letter_tone.lower(): generated_letter}
                        
                        st.success("✅ Cover letter(s) generated successfully!")
                        
                        # Silent tracking - Cover letter generation
                        cv_text = st.session_state.generated_cv if st.session_state.generated_cv else ""
                        if isinstance(st.session_state.generated_cover_letter, dict):
                            cover_letter_text = str(list(st.session_state.generated_cover_letter.values())[0])
                        else:
                            cover_letter_text = str(st.session_state.generated_cover_letter)
                        
                        silent_tracker.track_generation_results(
                            st.session_state.cv_content,
                            st.session_state.job_description,
                            cv_text,
                            cover_letter_text,
                            st.session_state.session_id,
                            st.session_state.get("company_name", "")
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error generating cover letter: {str(e)}")
        
        # Quick actions
        if st.session_state.cv_content and st.session_state.job_description:
            if st.button("🚀 Generate Both Documents", use_container_width=True):
                with st.spinner("Generating both documents..."):
                    try:
                        # Generate CV
                        cv_generator = CVGenerator()
                        user_preferences = {"focus_areas": cv_focus, "emphasize_keywords": True}
                        generated_cv = cv_generator.generate_tailored_cv(
                            st.session_state.cv_content,
                            st.session_state.job_description,
                            user_preferences
                        )
                        st.session_state.generated_cv = generated_cv
                        
                        # Generate Cover Letter
                        cover_letter_generator = CoverLetterGenerator()
                        company_info = {
                            "name": st.session_state.get("company_name", ""),
                            "hiring_manager": st.session_state.get("hiring_manager", ""),
                        }
                        
                        generated_letter = cover_letter_generator.generate_cover_letter(
                            st.session_state.cv_content,
                            st.session_state.job_description,
                            company_info,
                            tone=cover_letter_tone.lower()
                        )
                        st.session_state.generated_cover_letter = {cover_letter_tone.lower(): generated_letter}
                        
                        st.success("✅ Both documents generated successfully!")
                        
                        # Silent tracking - Both documents
                        silent_tracker.track_generation_results(
                            st.session_state.cv_content,
                            st.session_state.job_description,
                            generated_cv,
                            generated_letter,
                            st.session_state.session_id,
                            st.session_state.get("company_name", "")
                        )
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with tab3:
        st.markdown('<div class="section-header">Generated Documents</div>', unsafe_allow_html=True)
        
        # Preview controls
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**Preview Settings**")
            font_size = st.slider("Font Size", 10, 18, 14)
            line_spacing = st.slider("Line Spacing", 1.0, 2.0, 1.5)
        
        # Preview pane
        preview_style = f"font-size: {font_size}px; line-height: {line_spacing};"
        
        if st.session_state.generated_cv or st.session_state.generated_cover_letter:
            if preview_mode == "Full":
                if st.session_state.generated_cv:
                    st.markdown("### 📄 Tailored CV")
                    st.markdown(f'<div style="{preview_style} white-space: pre-wrap;">{st.session_state.generated_cv}</div>',
                                unsafe_allow_html=True)
                
                if st.session_state.generated_cover_letter:
                    st.markdown("### 💌 Cover Letter")
                    if isinstance(st.session_state.generated_cover_letter, dict):
                        version_key = list(st.session_state.generated_cover_letter.keys())[0]
                        st.markdown(f'<div style="{preview_style} white-space: pre-wrap;">{st.session_state.generated_cover_letter[version_key]}</div>',
                                    unsafe_allow_html=True)
            
            elif preview_mode == "Split View":
                col1, col2 = st.columns(2)
                with col1:
                    if st.session_state.generated_cv:
                        st.markdown("### 📄 CV Preview")
                        st.markdown(f'<div style="{preview_style} white-space: pre-wrap;">{st.session_state.generated_cv}</div>',
                                    unsafe_allow_html=True)
                with col2:
                    if st.session_state.generated_cover_letter:
                        st.markdown("### 💌 Cover Letter Preview")
                        if isinstance(st.session_state.generated_cover_letter, dict):
                            version_key = list(st.session_state.generated_cover_letter.keys())[0]
                            st.markdown(f'<div style="{preview_style} white-space: pre-wrap;">{st.session_state.generated_cover_letter[version_key]}</div>',
                                        unsafe_allow_html=True)
            
            elif preview_mode == "Diff Comparison" and st.session_state.cv_content and st.session_state.generated_cv:
                st.markdown("### 🔍 CV Comparison")
                original_lines = st.session_state.cv_content.split('\n')
                generated_lines = st.session_state.generated_cv.split('\n')
                
                for i in range(max(len(original_lines), len(generated_lines))):
                    original = original_lines[i] if i < len(original_lines) else ""
                    generated = generated_lines[i] if i < len(generated_lines) else ""
                    
                    if original != generated:
                        st.markdown(f'<div style="{preview_style} color: red;">- {original}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div style="{preview_style} color: green;">+ {generated}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="{preview_style}">  {original}</div>', unsafe_allow_html=True)
        
        # Download section
        st.markdown("---")
        st.markdown("### 📥 Download Documents")
        
        if st.session_state.generated_cv:
            st.download_button(
                label="Download Tailored CV",
                data=st.session_state.generated_cv,
                file_name=f"tailored_cv_{cv_tone.lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        if st.session_state.generated_cover_letter:
            if isinstance(st.session_state.generated_cover_letter, dict):
                for version, content in st.session_state.generated_cover_letter.items():
                    st.download_button(
                        label=f"Download {version.title()} Cover Letter",
                        data=content,
                        file_name=f"cover_letter_{version}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
    
    with tab4:
        st.markdown('<div class="section-header">Analytics & Insights</div>', unsafe_allow_html=True)
        
        if st.session_state.cv_content and st.session_state.job_description:
            CVAnalytics.display_analytics_dashboard(
                st.session_state.cv_content, 
                st.session_state.job_description
            )
        else:
            st.info("📊 Upload your CV and job description to see analytics.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        f"Made with 😍 using Streamlit & Groq | Version {settings.version}"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()