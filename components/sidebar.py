"""
Updated Sidebar component with URL fetching capability
"""

import streamlit as st
from utils.helpers import get_api_key, mask_api_key, show_success_message, show_info_message, show_warning_message, show_error_message
from utils.document_processing import process_uploaded_file
from config.constants import DEFAULT_RESUME as RESUME_FILENAME, DEFAULT_PROJECTS as PROJECTS_FILENAME

# Import the new job URL fetcher
try:
    from utils.job_url_fetcher import fetch_and_display_job, save_job_to_session
    URL_FETCHER_AVAILABLE = True
except ImportError:
    URL_FETCHER_AVAILABLE = False


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
    
    # Job Description Configuration with URL Fetching
    with st.expander("🎯 Configure Target Job Description", expanded=not st.session_state.jd_configured):
        st.markdown("**Choose your input method:**")
        
        # Create tabs for different input methods
        jd_tab1, jd_tab2 = st.tabs(["📝 Manual Entry", "🔗 Fetch from URL"])
        
        with jd_tab1:
            st.markdown("**Paste job description manually:**")
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
                help="This job description will be the default context for all operations",
                key="manual_jd_input"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Job Description", use_container_width=True, key="save_manual_jd"):
                    st.session_state.job_description = job_desc_input
                    st.session_state.jd_configured = True
                    if 'job_url' in st.session_state:
                        del st.session_state.job_url  # Clear URL if manually edited
                    show_success_message("Job description saved! All features will now use this as context.")
                    st.rerun()
            with col2:
                if st.button("🗑️ Clear Job Description", use_container_width=True, key="clear_manual_jd"):
                    st.session_state.job_description = ""
                    st.session_state.jd_configured = False
                    if 'job_url' in st.session_state:
                        del st.session_state.job_url
                    if 'job_details' in st.session_state:
                        del st.session_state.job_details
                    show_info_message("Job description cleared.")
                    st.rerun()
        
        with jd_tab2:
            if not URL_FETCHER_AVAILABLE:
                st.warning("⚠️ URL fetching not available. Install required packages:")
                st.code("pip install requests beautifulsoup4", language="bash")
            else:
                st.markdown("**Fetch job description from URL:**")
                st.info("📌 Supports: LinkedIn, Indeed, Greenhouse, Lever, and most job boards")
                
                job_url = st.text_input(
                    "Job Posting URL",
                    placeholder="https://www.linkedin.com/jobs/view/...",
                    help="Paste the URL of the job posting",
                    key="job_url_input"
                )
                
                fetch_button = st.button("🌐 Fetch Job Description", 
                                        use_container_width=True, 
                                        key="fetch_job_url",
                                        disabled=not job_url.strip())
                
                if fetch_button and job_url.strip():
                    # Store URL in session state to trigger display in main area
                    st.session_state.fetching_job_url = job_url
                    st.session_state.show_job_preview = True
                    st.rerun()
                
                # Show if job was fetched from URL
                if st.session_state.get('job_url'):
                    st.success(f"✅ Currently using job from URL")
                    st.caption(f"Source: {st.session_state.job_url[:50]}...")
                    
                    if st.button("🔄 Fetch Different Job", use_container_width=True, key="fetch_new_job"):
                        if 'fetching_job_url' in st.session_state:
                            del st.session_state.fetching_job_url
                        if 'show_job_preview' in st.session_state:
                            del st.session_state.show_job_preview
                        st.rerun()
        
        # Show configuration status
        if st.session_state.jd_configured:
            st.divider()
            st.success("✅ Job description is configured and active!")
            
            # Show source
            if 'job_url' in st.session_state:
                st.caption(f"📌 Source: Fetched from URL")
            else:
                st.caption(f"📌 Source: Manual entry")
    
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
    
    # RAG System Configuration
    st.subheader("🧠 Smart RAG System")
    
    st.markdown("""
    **Semantic Document Search** uses AI to find only relevant parts of your documents, 
    making responses more specific and reducing costs.
    """)
    
    use_rag = st.toggle(
        "Enable Smart Document Search (RAG)",
        value=st.session_state.get('use_rag', False),
        help="When enabled, uses semantic search to find relevant information instead of sending all documents every time",
        key="rag_toggle"
    )
    
    st.session_state.use_rag = use_rag
    
    if use_rag:
        # Import RAG utilities
        try:
            from utils.rag_system import (
                initialize_rag_system, 
                index_documents_if_needed
            )
            
            # Initialize RAG system
            rag_system = initialize_rag_system(api_key)
            
            # Auto-index if documents are loaded but not indexed
            if st.session_state.documents and not rag_system.chunks:
                with st.spinner("🔄 Indexing documents for smart search..."):
                    index_documents_if_needed(rag_system)
            
            # Show RAG statistics
            if rag_system.chunks:
                stats = rag_system.get_statistics()
                
                st.success("✅ RAG System Active")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Indexed Chunks", stats['total_chunks'])
                with col2:
                    st.metric("Documents", stats['total_documents'])
                
                st.metric("Avg Chunk Size", f"{stats['avg_chunk_size']} chars")
                
                with st.expander("📚 Indexed Documents"):
                    for source in stats['sources']:
                        st.text(f"✓ {source}")
                
                # Re-index button
                if st.button("🔄 Re-index All Documents", use_container_width=True):
                    rag_system.chunks = []
                    rag_system.embeddings_cache = {}
                    with st.spinner("Re-indexing..."):
                        index_documents_if_needed(rag_system)
                    show_success_message("Documents re-indexed successfully!")
                    st.rerun()
            else:
                st.info("📝 No documents indexed yet. Upload documents to enable RAG.")
        
        except ImportError as e:
            st.error("❌ RAG system not available. Install numpy: `pip install numpy`")
            st.session_state.use_rag = False
        except Exception as e:
            st.error(f"❌ Error initializing RAG: {str(e)}")
            st.session_state.use_rag = False
    else:
        st.info("📄 Standard mode: All documents sent with each request")
        st.caption("Toggle on to enable smart semantic search")
    
    st.divider()
    
    # Portfolio & GitHub Integration
    st.subheader("🌐 Portfolio & GitHub")
    
    portfolio_status = st.session_state.get('portfolio_loaded', False)
    
    if portfolio_status:
        st.success("✅ Portfolio content loaded")
        col1, col2 = st.columns(2)
        with col1:
            portfolio_url = st.session_state.get('portfolio_url', 'N/A')
            st.markdown(f"[🌐 Portfolio]({portfolio_url})")
        with col2:
            github_url = st.session_state.get('github_url', 'N/A')
            st.markdown(f"[💻 GitHub]({github_url})")
        
        if st.button("🔄 Refresh Portfolio Content", use_container_width=True):
            from utils.portfolio_fetcher import refresh_portfolio_content
            if refresh_portfolio_content():
                show_success_message("Portfolio content refreshed!")
                # Re-index if RAG is enabled
                if st.session_state.get('use_rag', False):
                    from utils.rag_system import initialize_rag_system, index_documents_if_needed
                    rag_system = initialize_rag_system(api_key)
                    rag_system.chunks = []
                    rag_system.embeddings_cache = {}
                    index_documents_if_needed(rag_system)
                st.rerun()
    else:
        st.info("📡 Portfolio content not loaded")
        if st.button("📥 Fetch Portfolio & GitHub", use_container_width=True):
            from utils.portfolio_fetcher import load_portfolio_content
            with st.spinner("Fetching content from web..."):
                if load_portfolio_content():
                    show_success_message("✅ Portfolio and GitHub content loaded!")
                    # Index if RAG is enabled
                    if st.session_state.get('use_rag', False):
                        from utils.rag_system import initialize_rag_system, index_documents_if_needed
                        rag_system = initialize_rag_system(api_key)
                        index_documents_if_needed(rag_system)
                    st.rerun()
                else:
                    st.error("❌ Could not fetch portfolio content. Check internet connection.")
    
    st.caption("Fetches live content from your portfolio website and GitHub profile")
    
    st.divider()
    
    # Document Status
    if st.session_state.documents:
        loaded_files = []
        if RESUME_FILENAME in st.session_state.documents:
            loaded_files.append(f"✅ Resume: {RESUME_FILENAME}")
        
        if PROJECTS_FILENAME in st.session_state.documents:
            loaded_files.append(f"✅ Projects: {PROJECTS_FILENAME}")
        
        if loaded_files:
            for file_info in loaded_files:
                st.success(file_info)
        
        additional_docs = len(st.session_state.documents) - len([f for f in [RESUME_FILENAME, PROJECTS_FILENAME] if f in st.session_state.documents])
        if additional_docs > 0:
            show_info_message(f"📄 {additional_docs} additional document(s) loaded")
    else:
        show_warning_message(f"⚠️ Default files not found")
        st.info("Please upload your resume and projects files manually below.")
    
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
                elif doc_name == PROJECTS_FILENAME:
                    st.text(f"🚀 {doc_name}")
                else:
                    st.text(doc_name)
            with col2:
                if st.button("🗑️", key=f"delete_{doc_name}"):
                    del st.session_state.documents[doc_name]
                    st.rerun()
    
    return api_key