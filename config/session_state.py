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

def clear_session_state():
    """Clear all session state variables"""
    keys_to_clear = [
        'documents', 'auto_loaded', 'job_description', 'jd_configured',
        'chat_history', 'personal_details', 'writing_guidelines'
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
