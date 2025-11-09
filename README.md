# AI Career Assistant

A powerful AI-powered career management application built with Streamlit and Google Gemini AI. This application helps job seekers create professional emails, update resumes, generate cover letters, and get personalized career advice.

## Features

### 📧 Email Writer
- Generate professional job application emails
- Multiple email purposes (Job Application, Follow-up, Networking, Thank You)
- Customizable tone (Professional, Confident, Friendly, Formal)
- Automatic technology matching with job requirements
- **NEW:** Send emails directly from the app using SMTP
- Supports Gmail, Outlook, Yahoo, AOL and more
- Uses app-specific passwords for secure authentication

### 📄 Resume Updater
- Tailor resume to specific job descriptions
- Update skills sections, summaries, and project highlights
- ATS-friendly formatting
- Keyword optimization

### ✉️ Cover Letter Generator
- Create compelling, personalized cover letters
- Automatic extraction of job details
- Professional formatting with proper signatures
- Technology and skill matching

### 💬 Q&A Assistant
- Personalized career advice based on your profile
- Job-specific insights and recommendations
- Resume and job description analysis

### 📊 Document Analysis
- Job match analysis
- Skills extraction and matching
- Project relevance assessment
- Career summary generation

## Setup

### Prerequisites
- Python 3.8+
- Google Gemini API Key

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd job_ai_agent
```

2. Install required packages:
```bash
pip install streamlit google-generativeai PyPDF2 python-docx python-dotenv
```

3. Configure your API key:
   - The application includes a default API key for testing
   - For production use, create a `.env` file with your own Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

4. Place your resume:
   - Add your resume file named `Vinay_Ramesh_full_stack_developer.pdf` in the project directory
   - Or upload it manually through the application interface

### Running the Application

```bash
streamlit run main.py
```

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Configure Job Description**: Enter your target job description once in the sidebar - it will be used across all features
2. **Upload Documents**: The app automatically loads your default resume, or you can upload additional documents
3. **Choose Your Task**: Use the tabs to access different features:
   - Email Writer: Create professional emails and send them directly
   - Resume Updater: Tailor your resume to job requirements
   - Cover Letter Generator: Create compelling cover letters
   - Q&A Assistant: Get personalized career advice
   - Document Analysis: Analyze your profile and job match

## 📮 Email Sending Feature

The Email Writer now supports sending emails directly from the application!

### How to Use:
1. Generate your email using the Email Writer
2. Click the "📮 Send Email" button
3. Enter your email and app password
4. Enter the recipient's email
5. Click "Send Email"

### Getting an App Password:

**For Gmail:**
1. Enable 2-Step Verification in your Google Account
2. Go to Security → App passwords
3. Generate a new 16-character app password
4. Use this password in the app (not your regular password!)

**For Outlook/Hotmail:**
1. Enable two-step verification at account.microsoft.com/security
2. Generate an app password
3. Use this password in the app

**For Other Providers:** Check your provider's security settings for app passwords.

## Key Features

- **One-time Setup**: Configure your job description once, use it across all features
- **Automatic Context**: AI uses your resume, personal details, and job requirements for all outputs
- **Professional Output**: All generated content follows professional writing guidelines
- **Technology Matching**: Automatically highlights relevant technologies and skills
- **F1 OPT Support**: Properly handles work authorization details for international students

## Personal Details Configuration

The application includes pre-configured personal details that can be edited in the sidebar:
- Full Name: Vinay Ramesh
- Email: vinayramesh6020@gmail.com
- Contact: +1 (682) 273-5833
- Education: MS Data Science (UNT), BTech Computer Science
- Location: Denton, TX
- Work Authorization: F1 OPT

## Writing Guidelines

The application follows specific writing guidelines to ensure:
- Professional, human-like tone
- Clean formatting without excessive markdown
- Technology and skill matching
- Proper email signatures
- Concise, impactful content

## Security

- API keys are handled securely
- Personal information is processed locally
- No data is stored permanently on external servers

## Contributing

This is a personal career assistant application. For suggestions or improvements, please contact the developer.

## License

Private project - All rights reserved.
