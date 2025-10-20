"""
AI Career Assistant - Main Application
A modular Streamlit application for career management powered by Gemini AI
"""

import streamlit as st

# Import configuration and utilities
from config.constants import PAGE_CONFIG, TABS, DEFAULT_RESUME, DEFAULT_PROJECTS
from config.session_state import initialize_session_state
from utils.helpers import setup_environment
from utils.document_processing import auto_load_default_resume, auto_load_projects_file, auto_load_additional_documents

# Import components
from components.sidebar import render_sidebar
from components.email_writer import render_email_writer
from components.resume_updater import render_resume_updater
from components.cover_letter import render_cover_letter
from components.qa_assistant import render_qa_assistant
from components.document_analysis import render_document_analysis


def render_job_preview():
    """Render job preview when fetching from URL"""
    if not st.session_state.get('show_job_preview', False):
        return False
    
    if not st.session_state.get('fetching_job_url'):
        return False
    
    try:
        from utils.job_url_fetcher import fetch_and_display_job, save_job_to_session
        
        st.info("🔍 **Job Description Preview** - Review the extracted information below")
        
        url = st.session_state.fetching_job_url
        job_details = fetch_and_display_job(url)
        
        if job_details:
            # Show action buttons
            st.divider()
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                if st.button("✅ Use This Job Description", 
                           use_container_width=True, 
                           type="primary",
                           key="use_fetched_jd_main"):
                    save_job_to_session(job_details)
                    # Clear preview flags
                    del st.session_state.fetching_job_url
                    del st.session_state.show_job_preview
                    st.success("✅ Job description configured from URL!")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Fetch Different Job", 
                           use_container_width=True,
                           key="refetch_jd_main"):
                    del st.session_state.fetching_job_url
                    del st.session_state.show_job_preview
                    st.rerun()
            
            with col3:
                if st.button("❌ Cancel", 
                           use_container_width=True,
                           key="cancel_jd_main"):
                    del st.session_state.fetching_job_url
                    del st.session_state.show_job_preview
                    st.rerun()
            
            return True
        else:
            st.error("❌ Could not fetch job description. Please try manual entry or a different URL.")
            if st.button("🔙 Go Back"):
                del st.session_state.fetching_job_url
                del st.session_state.show_job_preview
                st.rerun()
            return True
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        if st.button("🔙 Go Back"):
            if 'fetching_job_url' in st.session_state:
                del st.session_state.fetching_job_url
            if 'show_job_preview' in st.session_state:
                del st.session_state.show_job_preview
            st.rerun()
        return True


def main():
    """Main application function"""
    
    # Setup
    setup_environment()
    st.set_page_config(**PAGE_CONFIG)
    initialize_session_state()
    
    # Auto-load documents on first run
    if not st.session_state.auto_loaded:
        resume_loaded = auto_load_default_resume()
        projects_loaded = auto_load_projects_file()
        additional_loaded = auto_load_additional_documents()
        
        # Auto-load portfolio content
        if not st.session_state.get('portfolio_loaded', False):
            from utils.portfolio_fetcher import load_portfolio_content
            try:
                load_portfolio_content()
            except Exception as e:
                pass  # Silently fail, user can manually load later
        
        st.session_state.auto_loaded = True
    
    # Render sidebar and get API key
    with st.sidebar:
        api_key = render_sidebar()
    
    # Main Content
    st.title("💼 AI Career Assistant")
    st.markdown("*Your personal AI assistant for career management powered by Gemini*")
    
    # Check if we need to show job preview
    if render_job_preview():
        # Stop here and show only the preview
        return
    
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
        st.error(f"⚠️ No documents loaded. Please make sure your files are in the same folder as this script, or upload them manually in the sidebar.")
        st.info("""
        ### Getting Started:
        1. Place your resume file named `Vinay_Ramesh_full_stack_developer.pdf` in the same folder as this script
        2. Place your projects file named `My_projects.txt` in the same folder as this script
        3. Or upload your files manually using the sidebar
        4. Configure your target job description in the sidebar
        5. Choose a task from the tabs below once your documents are loaded
        """)
        st.stop()
    
    # Check if job description is configured
    if not st.session_state.jd_configured or not st.session_state.job_description.strip():
        st.warning("⚠️ Please configure your target job description first!")
        st.info("""
        ### Before You Begin:
        
        **📋 Configure your target job description in the sidebar** (under "🎯 Configure Target Job Description")
        
        Choose one of two methods:
        - **📝 Manual Entry**: Paste the job description directly
        - **🔗 Fetch from URL**: Automatically extract from job posting URL
        
        This is a **one-time setup** that will:
        - ✅ Generate tailored emails automatically
        - ✅ Update your resume to match the job requirements
        - ✅ Create customized cover letters
        - ✅ Provide job-specific career advice
        
        Simply configure once, and all features will use it as context!
        """)
        st.stop()
    
    # Show job description status
    st.success(f"✅ Target job configured! All features are using your job description as context.")
    
    # Show source information
    col1, col2 = st.columns([3, 1])
    with col1:
        with st.expander("📋 View Current Job Description"):
            job_desc_preview = st.session_state.job_description[:500] + "..." if len(st.session_state.job_description) > 500 else st.session_state.job_description
            st.text(job_desc_preview)
    
    with col2:
        if st.session_state.get('job_url'):
            st.caption("📌 Source: URL")
        else:
            st.caption("📌 Source: Manual")
    
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