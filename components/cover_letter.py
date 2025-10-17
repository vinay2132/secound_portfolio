"""
Cover Letter Generator component
"""

import streamlit as st
from utils.gemini_api import generate_content_with_context
from utils.helpers import download_button


def render_cover_letter(api_key):
    """Render the Cover Letter Generator tab"""
    
    st.header("✉️ Cover Letter Generator")
    st.markdown("Create compelling cover letters based on your configured job description.")
    st.info("💡 Using your configured job description as context")
    
    hiring_manager_cl = st.text_input(
        "Hiring Manager Name (optional)",
        placeholder="Leave empty if unknown",
        help="Enter the hiring manager's name if known",
        key="cl_hiring_manager"
    )
    
    why_interested = st.text_area(
        "Why are you interested in this position? (optional)",
        placeholder="Share your specific interest in this role or company...",
        height=100
    )
    
    if st.button("✨ Generate Cover Letter", key="generate_cl"):
        with st.spinner("Crafting your cover letter..."):
            prompt_template = """
TASK: Write a compelling cover letter for the TARGET JOB DESCRIPTION provided above

HIRING MANAGER: {hiring_manager}

WHY INTERESTED (if provided):
{why_interested}

Write a cover letter that:
- Uses "Dear Hiring Manager," if no specific name is provided, otherwise use the hiring manager's name
- Shows genuine interest in the role and company
- Highlights relevant experiences from my background that match the job requirements
- References specific projects from my PROJECT PORTFOLIO that demonstrate the required skills
- Matches specific technologies and skills from my resume to the job requirements
- Mentions concrete project achievements and outcomes that align with the job
- Is professional yet personable and human-sounding
- Mentions F1 OPT work authorization clearly when relevant
- Includes proper formatting: date, salutation, body paragraphs, closing
- Avoids generic phrases - make it authentic and specific
- Uses NO excessive bold text or highlighting
- Ends with my complete contact signature from the guidelines
- Keeps it concise but compelling (2-3 paragraphs maximum)

Write the cover letter now:
"""
            
            cover_letter = generate_content_with_context(
                prompt_template,
                api_key,
                hiring_manager=hiring_manager_cl if hiring_manager_cl else "Not provided - use 'Dear Hiring Manager,'",
                why_interested=why_interested
            )
            
            st.markdown("### Your Cover Letter:")
            st.text(cover_letter)
            
            # Download button
            download_button(
                label="📥 Download Cover Letter",
                data=cover_letter,
                file_name_prefix="cover_letter"
            )
