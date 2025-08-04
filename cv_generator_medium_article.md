# 🤖 Beginner's Guide to Building an AI-Powered CV Generator

## Introduction
In this tutorial, we'll build a smart CV generator that tailors your resume to specific job descriptions using AI. This project is perfect for beginners looking to explore AI application development with Python and Streamlit.

### What You'll Learn:
- Set up Python development environment
- Use Groq's lightning-fast LLMs
- Create a Streamlit web interface
- Deploy your app to the cloud

## Step 1: Environment Setup

### Install Python
First, install Python 3.9+ from the [official website](https://www.python.org/downloads/). During installation:
1. Check "Add Python to PATH"
2. Select "Custom installation" and include pip

Verify installation:
```bash
python --version
```

### Install Git
Download Git from [git-scm.com](https://git-scm.com/downloads) to manage our project code.

## Step 2: Project Setup

Clone the repository and install dependencies:
```bash
git clone https://github.com/yourusername/cv-generator.git
cd cv-generator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Configure API Access
Get your free Groq API key from [console.groq.com](https://console.groq.com) and add it to a `.env` file:
```env
GROQ_API_KEY=your_actual_key_here
```

## Step 4: Running the Application
Start the app with:
```bash
python run.py
```
Access it at `http://localhost:8501` in your browser.

## Step 5: Using the Application
1. **Upload your CV** (PDF, DOCX or TXT)
2. **Paste the job description**
3. **Select tone and focus areas**
4. **Generate tailored documents**
5. **Preview and download results**

## Step 6: Customization Options
### Change Templates
Modify the HTML templates in `app/templates/`:
- `cv_template.html` - CV layout
- `cover_letter_template.html` - Cover letter design

### Add New Features
The code is structured for easy extension:
- `app/services/` - AI generation logic
- `app/main.py` - Web interface
- `app/utils/` - Helper functions

## Step 7: Deploy to Streamlit Cloud
1. Create account at [share.streamlit.io](https://share.streamlit.io/)
2. Connect your GitHub repository
3. Set main file to `run.py`
4. Add Groq API key in secrets
5. Deploy!

Your app will be live at: `https://share.streamlit.io/yourusername/cv-generator`

## Troubleshooting Tips
- **Module errors**: Reactivate virtual environment with `source venv/bin/activate`
- **API issues**: Verify `.env` file location and key validity
- **Template problems**: Check file paths in `app/templates/`

## Conclusion
You've built an AI-powered CV generator that can be customized and deployed! This project demonstrates how to:
- Integrate LLMs into applications
- Create user-friendly interfaces with Streamlit
- Deploy AI applications to the cloud

For more advanced features, consider:
- Adding multiple template options
- Implementing PDF export
- Creating an analytics dashboard

Happy coding! 🚀