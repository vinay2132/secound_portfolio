"""
Resume Updater component for tailoring resumes to job descriptions
"""

import streamlit as st
from utils.gemini_api import generate_content_with_context
from utils.helpers import download_button


def render_resume_updater(api_key):
    """Render the Resume Updater tab"""
    
    st.header("📄 Resume Updater")
    st.markdown("Update your resume to match your configured job description.")
    st.info("💡 Using your configured job description as context")
    
    update_type = st.radio(
        "What would you like to update?",
        ["Tailor entire resume", "Update skills section", "Optimize summary", "Highlight relevant projects"]
    )
    
    additional_instructions = st.text_area(
        "Additional Instructions (optional)",
        placeholder="Any specific points to emphasize or changes to make...",
        height=100
    )
    
    if st.button("🔄 Update Resume", key="update_resume"):
        with st.spinner("Updating resume..."):
            prompt_template = """
TASK: {update_type}

Based on my background and the TARGET JOB DESCRIPTION provided above, {update_type_lower}.

ADDITIONAL INSTRUCTIONS:
{additional_instructions}

REQUIREMENTS:
- Highlight relevant skills and experiences that match the target job
- Use keywords from the job description naturally
- Maintain professional format WITHOUT excessive bold or highlighting
- Emphasize achievements that match the role
- Keep it concise and ATS-friendly
- Sound natural and human, not AI-generated

Provide the updated section or full resume:
"""
            
            updated_resume = generate_content_with_context(
                prompt_template,
                api_key,
                update_type=update_type,
                update_type_lower=update_type.lower(),
                additional_instructions=additional_instructions
            )
            
            st.markdown("### Updated Resume:")
            st.text(updated_resume)
            
            # Download button
            download_button(
                label="📥 Download Updated Resume",
                data=updated_resume,
                file_name_prefix="resume_updated"
            )
