"""
Constants and configuration values for the AI Career Assistant
"""

# API Configuration
DEFAULT_API_KEY = "AIzaSyD26rG9VpYFPmYCnQ_U8OO6jOKREzEZRYY"
GEMINI_MODEL = "gemini-2.0-flash-exp"

# File Configuration
DEFAULT_RESUME = "Vinay_Ramesh_full_stack_developer.pdf"
SUPPORTED_FILE_TYPES = ['pdf', 'docx', 'txt']

# Personal Details Template
PERSONAL_DETAILS_TEMPLATE = """
Full Name: Vinay Ramesh
Email: vinayramesh6020@gmail.com
Contact Number: +1 (682) 273-5833
Expected Rate: $60-$70/hr
Education: Master of Science in Data Science (UNT, Sep 2023 – Dec 2024), Bachelor of Technology in Computer Science (TKR College of Engineering & Technology, Jun 2017 – May 2021)
Current Location: Denton, TX
Relocation: Yes
Availability to Take Call: Yes
Availability to Join: Within 1-2 weeks
Relevant Experience: 3+ years in Full Stack Development
Visa/Work Authorization: F1 OPT
"""

# Writing Guidelines Template
WRITING_GUIDELINES_TEMPLATE = """
CRITICAL WRITING GUIDELINES - MUST FOLLOW FOR ALL OUTPUTS:

1. TONE & STYLE:
   - Write as a seasoned professional with 3+ years of experience
   - Make it sound HUMAN and natural, NOT AI-generated
   - Be professional, confident, and recruiter-friendly
   - Avoid over-formal or robotic language

2. FORMATTING RULES:
   - DO NOT use highlighting, bold text, asterisks (**), or excessive markdown
   - Keep content clean and simple
   - For emails: Include a relevant subject line at the top
   - Use proper paragraph spacing, but keep it minimal

3. EMAIL-SPECIFIC RULES:
   - Keep emails SHORT (1-2 concise paragraphs maximum)
   - Highlight specific technologies from BOTH job description and resume
   - If no hiring manager name is provided, use: "Dear Hiring Manager,"
   - ALWAYS mention F1 OPT work authorization clearly when relevant
   - ALWAYS use this exact signature format:

--
Best regards,
Vinay Ramesh
Senior Full Stack Developer
📧 vinayramesh6020@gmail.com
📞 +1 (682) 273-5833

4. CONTENT REQUIREMENTS:
   - Incorporate personal details naturally where relevant
   - Match technologies and skills to the job requirements
   - Be specific and avoid generic phrases
   - Show genuine interest and understanding of the role

5. GENERAL RULES FOR ALL OUTPUTS:
   - Prioritize clarity and readability
   - Use active voice
   - Be concise and to the point
   - Proofread for grammar and professionalism
"""

# Streamlit Page Configuration
PAGE_CONFIG = {
    "page_title": "AI Career Assistant",
    "page_icon": "💼",
    "layout": "wide"
}

# Tab Configuration
TABS = [
    "📧 Email Writer",
    "📄 Resume Updater", 
    "✉️ Cover Letter",
    "💬 Q&A Assistant",
    "📊 Document Summary"
]
