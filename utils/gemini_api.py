"""
Gemini API utilities and wrapper functions
"""

import streamlit as st
import google.generativeai as genai
from config.constants import GEMINI_MODEL


def call_gemini(prompt, api_key):
    """Call Gemini API with the given prompt"""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name=GEMINI_MODEL)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def get_context():
    """Build context from all uploaded documents, personal details, and guidelines"""
    context = f"""{st.session_state.writing_guidelines}

PERSONAL DETAILS:
{st.session_state.personal_details}

TARGET JOB DESCRIPTION:
{st.session_state.job_description}

RESUME AND DOCUMENTS:
"""
    # Prioritize resume and projects files for better context
    from config.constants import DEFAULT_RESUME, DEFAULT_PROJECTS
    
    # Add resume first if available
    if DEFAULT_RESUME in st.session_state.documents:
        context += f"\n--- {DEFAULT_RESUME} ---\n{st.session_state.documents[DEFAULT_RESUME]}\n"
    
    # Add projects file second if available
    if DEFAULT_PROJECTS in st.session_state.documents:
        context += f"\n--- {DEFAULT_PROJECTS} (PROJECT PORTFOLIO) ---\n{st.session_state.documents[DEFAULT_PROJECTS]}\n"
    
    # Add other documents
    for doc_name, doc_content in st.session_state.documents.items():
        if doc_name not in [DEFAULT_RESUME, DEFAULT_PROJECTS]:
            context += f"\n--- {doc_name} ---\n{doc_content}\n"
    
    return context


def generate_content_with_context(prompt_template, api_key, **kwargs):
    """Generate content using Gemini API with full context"""
    context = get_context()
    full_prompt = f"{context}\n\n{prompt_template.format(**kwargs)}"
    return call_gemini(full_prompt, api_key)
