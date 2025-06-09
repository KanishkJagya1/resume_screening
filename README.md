# HR AI Toolkit: Resume Screener & Employee Sentiment Analysis

A comprehensive AI-powered HR automation toolkit that leverages Google's Gemini API to streamline resume screening and employee sentiment analysis processes.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Overview

The HR AI Toolkit addresses two critical challenges in human resources management:

1. **Automated Resume Screening**: Intelligently matches candidates to job requirements using advanced natural language processing
2. **Employee Sentiment Analysis**: Analyzes employee feedback to provide actionable insights into workplace culture and morale

Built on Google's Gemini API, this toolkit provides enterprise-grade AI capabilities with a user-friendly Streamlit interface.

## Features

### Resume Screening Module
- **Intelligent Matching**: Advanced AI-powered candidate evaluation beyond simple keyword matching
- **Customizable Criteria**: Flexible screening parameters adaptable to specific role requirements
- **Batch Processing**: Efficient handling of multiple resumes simultaneously
- **Scoring System**: Quantitative candidate ranking with detailed justifications

### Sentiment Analysis Module
- **Multi-source Analysis**: Process surveys, feedback forms, and other textual data
- **Granular Categorization**: Detailed sentiment classification (positive, negative, neutral)
- **Theme Identification**: Automatic detection of underlying topics and concerns
- **Trend Analysis**: Historical sentiment tracking and reporting

### Technical Features
- **Scalable Architecture**: Handles workloads from small teams to enterprise deployments
- **RESTful API**: Optional API endpoints for system integration
- **Data Privacy**: Secure handling of sensitive HR information
- **Export Capabilities**: Results available in multiple formats (CSV, JSON, PDF)

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Core Services   │────│   Gemini API    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Data Storage   │────│  Processing      │────│  Configuration  │
│  (CSV/JSON)     │    │  Pipeline        │    │  Management     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Prerequisites

- Python 3.8 or higher
- Google Cloud account with Gemini API access
- 4GB+ RAM recommended for batch processing
- Internet connection for API calls

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/KanishkJagya1/resume_screening.git
cd resume_screening
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv hr_tech_env

# Activate virtual environment
# Windows
hr_tech_env\Scripts\activate

# macOS/Linux
source hr_tech_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python -c "import google.generativeai; print('Installation successful')"
```

## Configuration

### API Key Setup

#### Option 1: Environment Variable (Recommended for Production)

**Windows:**
```cmd
set GOOGLE_API_KEY=your_gemini_api_key_here
```

**macOS/Linux:**
```bash
export GOOGLE_API_KEY="your_gemini_api_key_here"
```

#### Option 2: .env File (Recommended for Development)

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key_here
DEBUG=True
MAX_BATCH_SIZE=50
```

### Additional Configuration

Modify `config/settings.py` to customize:
- API rate limits
- Batch processing sizes
- Output formats
- Model parameters

## Usage

### Starting the Application

```bash
streamlit run main.py
```

The application will be available at `http://localhost:8501`

### Resume Screening Workflow

1. **Upload Job Description**: Paste or upload the job requirements
2. **Upload Resumes**: Batch upload candidate resumes (PDF, DOCX, TXT)
3. **Configure Screening**: Set matching criteria and weights
4. **Process & Review**: Analyze results and export rankings

### Sentiment Analysis Workflow

1. **Data Input**: Upload employee feedback files or paste text directly
2. **Analysis Configuration**: Select analysis depth and categories
3. **Process Data**: Run sentiment analysis across all inputs
4. **Generate Reports**: View insights and export detailed reports

### Command Line Interface

For automated workflows:

```bash
# Resume screening
python -m src.resume_screening.cli --job-desc job.txt --resumes data/resumes/ --output results.csv

# Sentiment analysis
python -m src.sentiment_analysis.cli --input feedback.csv --output sentiment_report.json
```

## Project Structure

```
hr-ai-toolkit/
├── api/                    # REST API endpoints
│   ├── __init__.py
│   ├── resume_api.py
│   └── sentiment_api.py
├── config/                 # Configuration files
│   ├── __init__.py
│   └── settings.py
├── data/                   # Sample data and outputs
│   ├── input/
│   ├── output/
│   └── samples/
├── src/                    # Core application logic
│   ├── __init__.py
│   ├── resume_screening/   # Resume screening module
│   │   ├── __init__.py
│   │   ├── screener.py
│   │   ├── processor.py
│   │   └── cli.py
│   ├── sentiment_analysis/ # Sentiment analysis module
│   │   ├── __init__.py
│   │   ├── analyzer.py
│   │   ├── processor.py
│   │   └── cli.py
│   └── utils/              # Shared utilities
│       ├── __init__.py
│       ├── file_handler.py
│       └── api_client.py
├── tests/                  # Test suites
│   ├── __init__.py
│   ├── test_resume_screening.py
│   ├── test_sentiment_analysis.py
│   └── test_integration.py
├── .env.example           # Environment variables template
├── .gitignore
├── main.py                # Streamlit application entry point
├── requirements.txt       # Python dependencies
└── README.md
```

## API Documentation

### Resume Screening Endpoint

```http
POST /api/v1/screen-resumes
Content-Type: application/json

{
  "job_description": "Software Engineer position...",
  "resumes": ["resume1_text", "resume2_text"],
  "criteria": {
    "required_skills": ["Python", "SQL"],
    "experience_years": 3,
    "education_level": "Bachelor"
  }
}
```

### Sentiment Analysis Endpoint

```http
POST /api/v1/analyze-sentiment
Content-Type: application/json

{
  "texts": ["Employee feedback text 1", "Employee feedback text 2"],
  "analysis_type": "detailed",
  "categories": ["satisfaction", "workload", "management"]
}
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run specific module tests
python -m pytest tests/test_resume_screening.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Performance Considerations

- **Batch Size**: Limit batch processing to 50 items for optimal performance
- **Rate Limiting**: API calls are automatically throttled to respect Gemini API limits
- **Caching**: Processed results are cached to avoid redundant API calls
- **Memory Usage**: Large file processing is handled in chunks to manage memory consumption

## Security & Privacy

- API keys are never logged or stored in plain text
- Employee data is processed in memory and not persisted unless explicitly requested
- All API communications use HTTPS encryption
- Optional data anonymization features available

## Troubleshooting

### Common Issues

**API Key Issues:**
```bash
# Verify API key is set
python -c "import os; print('API Key:', os.getenv('GOOGLE_API_KEY', 'Not Set'))"
```

**Memory Issues:**
- Reduce batch size in configuration
- Process files individually for large datasets

**API Rate Limits:**
- Enable rate limiting in settings
- Implement exponential backoff (included by default)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run linting
flake8 src/ tests/
black src/ tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [Wiki Pages](https://github.com/KanishkJagya1/resume_screening/wiki)
- **Issues**: [GitHub Issues](https://github.com/KanishkJagya1/resume_screening/issues)
- **Discussions**: [GitHub Discussions](https://github.com/KanishkJagya1/resume_screening/discussions)

## Acknowledgments

- Google Gemini API for providing advanced language model capabilities
- Streamlit team for the excellent web application framework
- Contributors and beta testers who helped improve this toolkit

---

**Made with ❤️ for the HR community**