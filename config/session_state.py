"""
Session state initialization and management
"""

import streamlit as st

def initialize_session_state():
    """Initialize all session state variables with default values"""
    
    # Document management
    if 'documents' not in st.session_state:
        st.session_state.documents = {}
    if 'auto_loaded' not in st.session_state:
        st.session_state.auto_loaded = False
    
    # Job description management
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'jd_configured' not in st.session_state:
        st.session_state.jd_configured = False
    
    # Chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Personal details and guidelines
    if 'personal_details' not in st.session_state:
        from .constants import PERSONAL_DETAILS_TEMPLATE
        st.session_state.personal_details = PERSONAL_DETAILS_TEMPLATE
    
    if 'writing_guidelines' not in st.session_state:
        from .constants import WRITING_GUIDELINES_TEMPLATE
        st.session_state.writing_guidelines = WRITING_GUIDELINES_TEMPLATE
    
    # Portfolio & GitHub
    if 'portfolio_loaded' not in st.session_state:
        st.session_state.portfolio_loaded = False
    if 'portfolio_url' not in st.session_state:
        st.session_state.portfolio_url = "https://vinay2132.github.io/my_portfolio/"
    if 'github_url' not in st.session_state:
        st.session_state.github_url = "https://github.com/vinay2132"
    if 'portfolio_links' not in st.session_state:
        st.session_state.portfolio_links = ""

def clear_session_state():
    """Clear all session state variables"""
    keys_to_clear = [
        'documents', 'auto_loaded', 'job_description', 'jd_configured',
        'chat_history', 'personal_details', 'writing_guidelines',
        'use_rag', 'rag_system',  # RAG-related keys
        'portfolio_loaded', 'portfolio_url', 'github_url', 'portfolio_links'  # Portfolio keys
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]