"""
Email Writer component for generating professional emails
"""

import streamlit as st
from utils.gemini_api import generate_content_with_context
from utils.helpers import download_button


def render_email_writer(api_key):
    """Render the Email Writer tab"""
    
    st.header("📧 Professional Email Writer")
    st.markdown("Generate professional emails based on your configured job description.")
    st.info("💡 Using your configured job description as context")
    
    col1, col2 = st.columns(2)
    with col1:
        email_purpose = st.selectbox(
            "Email Purpose",
            ["Job Application", "Follow-up", "Networking", "Thank You", "Custom"]
        )
    with col2:
        email_tone = st.selectbox(
            "Tone",
            ["Professional", "Confident", "Friendly", "Formal"]
        )
    
    hiring_manager_name = st.text_input(
        "Hiring Manager Name (optional)",
        placeholder="Leave empty if unknown - will use 'Dear Hiring Manager,'",
        help="Enter the hiring manager's name if known"
    )
    
    additional_context = st.text_area(
        "Additional Context (optional)",
        placeholder="Add any extra details or specific points you want to mention...",
        height=100
    )
    
    if st.button("✨ Generate Email", key="generate_email"):
        with st.spinner("Generating email..."):
            salutation = f"Dear {hiring_manager_name}," if hiring_manager_name else "Dear Hiring Manager,"
            
            prompt_template = """
TASK: Write a {email_tone} job application email for: {email_purpose}

SALUTATION: {salutation}

ADDITIONAL CONTEXT (if provided):
{additional_context}

REQUIREMENTS:
- Start with: Subject: [create a short, relevant subject line]
- Use the salutation: {salutation}
- Keep it to 1-2 SHORT paragraphs maximum
- Highlight specific technologies that match BOTH the target job description and my resume
- Clearly mention F1 OPT work authorization
- End with the EXACT signature format from the guidelines
- Make it sound human, natural, and confident
- NO bold text, asterisks, or highlighting
- Reference the TARGET JOB DESCRIPTION provided in the context

Generate the email now:
"""
            
            email = generate_content_with_context(
                prompt_template, 
                api_key,
                email_tone=email_tone,
                email_purpose=email_purpose,
                salutation=salutation,
                additional_context=additional_context
            )
            
            st.markdown("### Generated Email:")
            st.text(email)
            
            # Download button
            download_button(
                label="📥 Download Email",
                data=email,
                file_name_prefix="email"
            )
