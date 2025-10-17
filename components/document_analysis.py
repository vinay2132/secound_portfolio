"""
Document Analysis component for insights and summaries
"""

import streamlit as st
from utils.gemini_api import generate_content_with_context
from utils.helpers import download_button


def render_document_analysis(api_key):
    """Render the Document Analysis tab"""
    
    st.header("📊 Document Summary & Analysis")
    st.markdown("Get insights and summaries based on your documents and target job.")
    st.info("💡 Analysis will include job match assessment")
    
    analysis_type = st.selectbox(
        "What would you like to analyze?",
        [
            "Job match analysis",
            "Project portfolio analysis",
            "Extract key skills matching the job",
            "List relevant projects for this job",
            "Compare my projects to job requirements",
            "Identify strengths and gaps for this role",
            "Generate career summary for this position",
            "Summarize all documents"
        ]
    )
    
    if st.button("📊 Analyze", key="analyze_docs"):
        with st.spinner("Analyzing your documents..."):
            prompt_template = """
TASK: {analysis_type}

Provide a comprehensive analysis based on the request, considering:
- My resume and documents
- My PROJECT PORTFOLIO with detailed project information
- The TARGET JOB DESCRIPTION
- How well I match the job requirements
- Which specific projects demonstrate the required skills

Be specific, detailed, and actionable:
- Reference specific projects from my portfolio when relevant
- Keep formatting clean and minimal
- Make it professional and easy to read
- Avoid excessive bold text or highlighting
- Provide concrete recommendations where applicable

Generate the analysis:
"""
            
            analysis = generate_content_with_context(
                prompt_template,
                api_key,
                analysis_type=analysis_type
            )
            
            st.markdown("### Analysis Results:")
            st.markdown(analysis)
            
            # Download button
            download_button(
                label="📥 Download Analysis",
                data=analysis,
                file_name_prefix="analysis"
            )
