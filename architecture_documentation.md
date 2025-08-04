# CV Generator Architecture Documentation

## System Architecture Overview
```mermaid
graph TD
    A[User] --> B[Streamlit UI]
    B --> C[CV Generator Service]
    B --> D[Cover Letter Service]
    C --> E[LLM Service]
    D --> E
    E --> F[Groq API]
    C --> G[CV Templates]
    D --> H[Cover Letter Templates]
    B --> I[Google Tracker]
    I --> J[Google Sheets]
```

## Document Generation Sequence
```mermaid
sequenceDiagram
    participant User
    participant Streamlit
    participant CVGenerator
    participant LLMService
    participant GroqAPI
    
    User->>Streamlit: Upload CV + Job Description
    Streamlit->>CVGenerator: Generate Tailored CV
    CVGenerator->>LLMService: Create Optimization Prompt
    LLMService->>GroqAPI: Send Request
    GroqAPI-->>LLMService: Return Optimized CV
    LLMService-->>CVGenerator: Processed Content
    CVGenerator-->>Streamlit: Generated CV
    Streamlit-->>User: Display Results
```

## Component Relationships
```mermaid
classDiagram
    class CVGenerator{
        +generate_tailored_cv()
        -parse_cv_content()
    }
    class CoverLetterGenerator{
        +generate_cover_letter()
    }
    class LLMService{
        +generate_response()
    }
    class GoogleTracker{
        +track_cv_upload()
        +track_generation_results()
    }
    
    CVGenerator --> LLMService
    CoverLetterGenerator --> LLMService
    GoogleTracker --> CVGenerator
    GoogleTracker --> CoverLetterGenerator
```

## Data Flow Graph
```mermaid
flowchart LR
    A[User Input] --> B(Streamlit UI)
    B --> C{Processing}
    C --> D[CV Generation]
    C --> E[Cover Letter Generation]
    D --> F[Template Application]
    E --> F
    F --> G[Output Rendering]
    G --> H[User Download]
    C --> I[Analytics Tracking]
    I --> J[Google Sheets]
```

## Key Architecture Papers
1. **AI-Powered Document Generation** - Explains the prompt engineering and optimization techniques
2. **Streamlit Architecture Patterns** - Details the UI component design
3. **LLM Integration Best Practices** - Covers efficient API usage and error handling
4. **Template System Design** - Documents the template engine implementation

All diagrams are available in Mermaid format for easy modification. You can view them directly on GitHub or import into Mermaid-compatible tools.