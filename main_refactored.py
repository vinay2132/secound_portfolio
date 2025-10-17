"""
AI Career Assistant - Main Application
A modular Streamlit application for career management powered by Gemini AI
"""

import streamlit as st

# Import configuration and utilities
from config.constants import PAGE_CONFIG, TABS, DEFAULT_RESUME
from config.session_state import initialize_session_state
from utils.helpers import setup_environment
from utils.document_processing import auto_load_default_resume, auto_load_additional_documents

# Import components
from components.sidebar import render_sidebar
from components.email_writer import render_email_writer
from components.resume_updater import render_resume_updater
from components.cover_letter import render_cover_letter
from components.qa_assistant import render_qa_assistant
from components.document_analysis import render_document_analysis


def main():
    """Main application function"""
    
    # Setup
    setup_environment()
    st.set_page_config(**PAGE_CONFIG)
    initialize_session_state()
    
    # Auto-load documents on first run
    if not st.session_state.auto_loaded:
        resume_loaded = auto_load_default_resume()
        additional_loaded = auto_load_additional_documents()
        st.session_state.auto_loaded = True
    
    # Render sidebar and get API key
    with st.sidebar:
        api_key = render_sidebar()
    
    # Main Content
    st.title("💼 AI Career Assistant")
    st.markdown("*Your personal AI assistant for career management powered by Gemini*")
    
    # Check for API key
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar or add it to your .env file.")
        st.info("""
        ### How to setup:
        1. Create a `.env` file in the same folder
        2. Add this line: `GEMINI_API_KEY=your_api_key_here`
        3. Or enter the key manually in the sidebar
        
        Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
        """)
        st.stop()
    
    # Check if documents are loaded
    if not st.session_state.documents:
        st.error(f"⚠️ No documents loaded. Please make sure '{DEFAULT_RESUME}' is in the same folder as this script, or upload your resume manually in the sidebar.")
        st.info("""
        ### Getting Started:
        1. Place your resume file named `Vinay_Ramesh_full_stack_developer.pdf` in the same folder as this script
        2. Or upload your resume manually using the sidebar
        3. Configure your target job description in the sidebar
        4. Choose a task from the tabs below once your documents are loaded
        """)
        st.stop()
    
    # Check if job description is configured
    if not st.session_state.jd_configured or not st.session_state.job_description.strip():
        st.warning("⚠️ Please configure your target job description first!")
        st.info("""
        ### Before You Begin:
        
        **📋 Configure your target job description in the sidebar** (under "🎯 Configure Target Job Description")
        
        This is a **one-time setup** that will:
        - ✅ Generate tailored emails automatically
        - ✅ Update your resume to match the job requirements
        - ✅ Create customized cover letters
        - ✅ Provide job-specific career advice
        
        Simply paste the complete job posting once, and all features will use it as context!
        """)
        st.stop()
    
    # Show job description status
    st.success(f"✅ Target job configured! All features are using your job description as context.")
    with st.expander("📋 View Current Job Description"):
        job_desc_preview = st.session_state.job_description[:500] + "..." if len(st.session_state.job_description) > 500 else st.session_state.job_description
        st.text(job_desc_preview)
    
    # Create tabs for different functionalities
    tab1, tab2, tab3, tab4, tab5 = st.tabs(TABS)
    
    # Tab 1: Email Writer
    with tab1:
        render_email_writer(api_key)
    
    # Tab 2: Resume Updater
    with tab2:
        render_resume_updater(api_key)
    
    # Tab 3: Cover Letter Generator
    with tab3:
        render_cover_letter(api_key)
    
    # Tab 4: Q&A Assistant
    with tab4:
        render_qa_assistant(api_key)
    
    # Tab 5: Document Analysis
    with tab5:
        render_document_analysis(api_key)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>💼 AI Career Assistant | Powered by Google Gemini</p>
        <p style='font-size: 0.8em;'>Your data is processed securely and not stored permanently.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
