# 🤖 AI CV & Cover Letter Generator

An intelligent application that generates tailored CVs and cover letters using AI, built with LangChain, Groq, and Streamlit.

## ✨ Features

- **Smart CV Tailoring**: Automatically adapts your CV to match job requirements
- **AI Cover Letters**: Generates personalized cover letters with different tones
- **Multiple Formats**: Supports PDF, DOCX, and TXT file uploads
- **Keyword Analysis**: Shows how well your CV matches the job description
- **Professional Templates**: Clean, ATS-friendly formatting
- **Multi-version Generation**: Create multiple cover letter variations
- **Docker Support**: Easy deployment with containerization

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/cv-generator.git
cd cv-generator
```

2. **Set up environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

4. **Run the application**
```bash
python run.py
```

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Or build manually**
```bash
docker build -t cv-generator .
docker run -p 8501:8501 --env-file .env cv-generator
```

### Heroku Deployment

1. **Create Heroku app**
```bash
heroku create your-app-name
heroku stack:set container
```

2. **Set environment variables**
```bash
heroku config:set GROQ_API_KEY=your_groq_api_key
```

3. **Deploy**
```bash
git push heroku main
```

## 🔧 Configuration

### Environment Variables

- `GROQ_API_KEY`: Your Groq API key (required)
- `STREAMLIT_SERVER_PORT`: Port for Streamlit (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Server address (default: 0.0.0.0)

### API Keys

Get your Groq API key from [console.groq.com](https://console.groq.com)

## 📱 Usage

1. **Upload your CV** or paste content directly
2. **Add job description** for the position you're applying to
3. **Configure settings** like tone and focus areas
4. **Generate documents** with AI-powered customization
5. **Download results** in your preferred format

## 🏗️ Architecture

```
cv-generator/
├── app/
│   ├── main.py              # Streamlit interface
│   ├── services/            # AI generation services
│   ├── utils/               # Utilities and helpers
│   └── templates/           # Document templates
├── config/                  # Configuration management
├── tests/                   # Unit tests
├── Dockerfile              # Container configuration
└── requirements.txt        # Python dependencies
```

## 🧪 Testing

```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- Check the [Issues](https://github.com/yourusername/cv-generator/issues) page
- Read the [Documentation](https://github.com/yourusername/cv-generator/wiki)
- Contact: [your-email@example.com](mailto:your-email@example.com)

## 🙏 Acknowledgments

- [LangChain](https://langchain.com) for the AI framework
- [Groq](https://groq.com) for high-speed inference
- [Streamlit](https://streamlit.io) for the web interface