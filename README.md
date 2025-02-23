# ElevateCV - AI-Powered Career Preparation Assistant 🚀

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://resumehack.streamlit.app/)
[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=flat&logo=github&logoColor=white)](https://github.com/datasciritwik/prepai)

## Overview

ElevateCV is an intelligent career preparation assistant that helps job seekers optimize their resumes, analyze skill gaps, and improve their job application materials using advanced AI technology.

## Features 🌟

### 1. Resume Analysis
- **ATS Score Calculation**: Get your resume's ATS (Applicant Tracking System) compatibility score
- **Keyword Optimization**: Identify and optimize keywords for better visibility
- **Format Checking**: Ensure your resume follows ATS-friendly formatting

### 2. Skill Gap Analysis
- Compare your skills against job requirements
- Identify missing critical skills
- Get personalized recommendations for skill development

### 3. Resume Optimization
- Receive tailored suggestions for improvement
- Optimize content for ATS systems
- Enhance professional presentation

### 4. Cover Letter Generation
- Generate customized cover letters
- Match content with job requirements
- Maintain professional tone and structure

### 5. Interactive Q&A
- Get instant answers to career-related questions
- Receive personalized advice
- Access context-aware responses based on your profile

## Technology Stack 💻

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/ML**: LangChain
- **LLM**: IBM Cloud Granite modesl
- **UI Components**: Streamlit components, MarkdownLit

## Getting Started 🚀

### Installation
1. Clone the repository

```
git clone https://github.com/datasciritwik/prepai.git

```
```
cd prepai
```


2. Install dependencies

```
pip install -r requirements.txt
```


3. Set up environment variables

```
cp .env.example .env
```

Add your API keys and configurations
```
WATSONX_APIKEY =""
PROJECT_ID = ""
```

Run the application : 
```
streamlit run prepai/main.py
```


## Usage Guide 📖

1. **Upload Resume**
   - Support for PDF and DOCX formats
   - Automatic text extraction

2. **Add Job Description**
   - Paste job description text
   - Get instant analysis

3. **View Analysis**
   - Check ATS score
   - Review skill gaps
   - Get optimization suggestions

4. **Generate Documents**
   - Create custom cover letters
   - Get optimized resume versions

5. **Ask Questions**
   - Use the chat interface for specific queries
   - Get personalized career advice

## Project Structure 📁
```
prepai/
|
├── Home.py # Main application entry
├── pages/
│ ├── qna.py # Q&A interface
│ └── ... # Other page components
├── modules/
│ ├── llm_connector.py # AI model integration
│ ├── result_generator.py # Analysis generation
│ └── page_utils.py # Utility functions

```




## Live Demo 🌐

Try ElevateCV now at [https://prepai.streamlit.app](https://resumehack.streamlit.app/)

## Contributing 🤝

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 💬

For support, please open an issue in the GitHub repository or contact us at [kshitijk146@gmail.com](mailto:kshitijk146@gmail.com)

## Acknowledgments 🙏

- Thanks to all contributors - Kshitij, Ritwik, Gifty
- Built with [Streamlit](https://streamlit.io/)
- Powered by IBM Granite Models 

---
Made with ❤️ by Aifans
