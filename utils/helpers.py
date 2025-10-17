"""
General helper functions and utilities
"""

import streamlit as st
from datetime import datetime
import os
from dotenv import load_dotenv
from config.constants import DEFAULT_API_KEY


def setup_environment():
    """Load environment variables"""
    load_dotenv()


def get_api_key():
    """Get API key from environment or return default"""
    env_api_key = os.getenv('GEMINI_API_KEY')
    return env_api_key if env_api_key else DEFAULT_API_KEY


def mask_api_key(api_key):
    """Mask API key for display purposes"""
    return api_key[:8] + "..." + api_key[-4:] if api_key else "Not configured"


def format_timestamp():
    """Get formatted timestamp for file naming"""
    return datetime.now().strftime('%Y%m%d_%H%M%S')


def download_button(label, data, file_name_prefix, file_extension="txt", mime_type="text/plain"):
    """Create a download button with standardized naming"""
    timestamp = format_timestamp()
    file_name = f"{file_name_prefix}_{timestamp}.{file_extension}"
    
    return st.download_button(
        label=label,
        data=data,
        file_name=file_name,
        mime=mime_type
    )


def show_success_message(message):
    """Display a success message"""
    st.success(message)


def show_error_message(message):
    """Display an error message"""
    st.error(message)


def show_warning_message(message):
    """Display a warning message"""
    st.warning(message)


def show_info_message(message):
    """Display an info message"""
    st.info(message)
