"""
Sidebar component for configuration and document management
"""

import streamlit as st
from utils.helpers import get_api_key, mask_api_key, show_success_message, show_info_message, show_warning_message
from utils.document_processing import process_uploaded_file, DEFAULT_RESUME
from config.constants import DEFAULT_RESUME as RESUME_FILENAME


def render_sidebar():
    """Render the sidebar with all configuration options"""
    
    # API Key Configuration
    st.title("⚙️ Configuration")
    
    env_api_key = st.session_state.get('env_api_key', None)
    api_key = get_api_key()
    
    if env_api_key:
        st.success("✅ API Key loaded from .env file")
        api_key = env_api_key
        masked_key = mask_api_key(env_api_key)
        st.text(f"Key: {masked_key}")
    else:
        api_key = api_key
        st.success("✅ Using default API Key")
        masked_key = mask_api_key(api_key)
        st.text(f"Key: {masked_key}")
        
        custom_key = st.text_input("Override API Key (optional)", type="password", 
                                 help="Leave empty to use default key")
        if custom_key:
            api_key = custom_key
    
    st.divider()
    
    # Job Description Configuration
    with st.expander("🎯 Configure Target Job Description", expanded=not st.session_state.jd_configured):
        st.markdown("**Enter the job description once - it will be used across all features:**")
        job_desc_input = st.text_area(
            "Job Description",
            value=st.session_state.job_description,
            height=300,
            placeholder="""Paste the complete job description here including:
- Job title and company name
- Requirements and qualifications
- Technologies and skills needed
- Job responsibilities
- Any other relevant details

This will be used for all email generation, resume updates, and cover letters.""",
            help="This job description will be the default context for all operations"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Job Description", use_container_width=True):
                st.session_state.job_description = job_desc_input
                st.session_state.jd_configured = True
                show_success_message("Job description saved! All features will now use this as context.")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Job Description", use_container_width=True):
                st.session_state.job_description = ""
                st.session_state.jd_configured = False
                show_info_message("Job description cleared.")
                st.rerun()
        
        if st.session_state.jd_configured:
            show_success_message("✅ Job description is configured and active!")
    
    st.divider()
    
    # Personal Details Editor
    with st.expander("✏️ Edit Personal Details"):
        st.markdown("**Update your personal information:**")
        personal_details_input = st.text_area(
            "Personal Details",
            value=st.session_state.personal_details,
            height=300,
            help="Edit your personal details that will be used in all generated content"
        )
        if st.button("💾 Save Personal Details"):
            st.session_state.personal_details = personal_details_input
            show_success_message("Personal details updated!")
            st.rerun()
    
    st.divider()
    
    # Document Status
    if st.session_state.documents:
        if RESUME_FILENAME in st.session_state.documents:
            show_success_message(f"✅ Default resume loaded: {RESUME_FILENAME}")
        
        additional_docs = len(st.session_state.documents) - (1 if RESUME_FILENAME in st.session_state.documents else 0)
        if additional_docs > 0:
            show_info_message(f"📄 {additional_docs} additional document(s) loaded")
    else:
        show_warning_message(f"⚠️ Default resume not found: {RESUME_FILENAME}")
        st.info("Please upload your resume manually below.")
    
    # Document Upload Section
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Resume or Additional Documents",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Upload your resume or additional documents"
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.documents:
                text = process_uploaded_file(file)
                if text:
                    st.session_state.documents[file.name] = text
                    show_success_message(f"✅ {file.name} uploaded!")
    
    # Display all loaded documents
    if st.session_state.documents:
        st.divider()
        st.subheader("📚 Loaded Documents")
        for doc_name in st.session_state.documents.keys():
            col1, col2 = st.columns([3, 1])
            with col1:
                if doc_name == RESUME_FILENAME:
                    st.text(f"⭐ {doc_name}")
                else:
                    st.text(doc_name)
            with col2:
                if st.button("🗑️", key=f"delete_{doc_name}"):
                    del st.session_state.documents[doc_name]
                    st.rerun()
    
    return api_key
