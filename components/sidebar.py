"""
Updated Sidebar component with URL fetching capability (Fixed - No Nested Expanders)
"""

import streamlit as st
from utils.helpers import (
    get_api_key,
    mask_api_key,
    show_success_message,
    show_info_message,
    show_warning_message,
    show_error_message
)
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

    # === API Key Configuration ===
    st.title("⚙️ Configuration")

    env_api_key = st.session_state.get('env_api_key', None)
    api_key = get_api_key()

    if env_api_key:
        st.success("✅ API Key loaded from .env file")
        api_key = env_api_key
        st.text(f"Key: {mask_api_key(env_api_key)}")
    else:
        st.success("✅ Using default API Key")
        st.text(f"Key: {mask_api_key(api_key)}")

        custom_key = st.text_input(
            "Override API Key (optional)",
            type="password",
            help="Leave empty to use default key"
        )
        if custom_key:
            api_key = custom_key

    st.divider()

    # === Job Description Configuration ===
    st.header("🎯 Configure Target Job Description")
    st.markdown("Choose your input method:")

    # Tabs for input methods
    jd_tab1, jd_tab2 = st.tabs(["📝 Manual Entry", "🔗 Fetch from URL"])

    # --- Manual Entry Tab ---
    with jd_tab1:
        st.markdown("**Paste job description manually:**")
        job_desc_input = st.text_area(
            "Job Description",
            value=st.session_state.job_description,
            height=300,
            placeholder="Paste full job description here...",
            key="manual_jd_input"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Save Job Description", use_container_width=True):
                st.session_state.job_description = job_desc_input
                st.session_state.jd_configured = True
                if "job_url" in st.session_state:
                    del st.session_state.job_url
                show_success_message("Job description saved! All features will use this as context.")
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Job Description", use_container_width=True):
                st.session_state.job_description = ""
                st.session_state.jd_configured = False
                for key in ["job_url", "job_details"]:
                    st.session_state.pop(key, None)
                show_info_message("Job description cleared.")
                st.rerun()

    # --- URL Fetching Tab ---
    with jd_tab2:
        if not URL_FETCHER_AVAILABLE:
            st.warning("⚠️ URL fetching not available. Install required packages:")
            st.code("pip install requests beautifulsoup4", language="bash")
        else:
            st.markdown("**Fetch content from ANY URL:**")
            st.success("✅ Works with job boards, career pages, and any website!")

            # Supported sources (use help text instead of nested expander)
            st.info(
                """
                **Optimized for Job Boards:**
                - LinkedIn, Indeed, Glassdoor, Workday
                - Greenhouse, Lever, Monster, Dice, ZipRecruiter

                **Also works with:**
                - Any job posting URL
                - Company websites or general web pages
                - Career portals

                Extracts: job titles, descriptions, requirements, skills, benefits.
                """
            )

            job_url = st.text_input(
                "Website URL",
                placeholder="https://example.com/jobs/software-engineer",
                key="job_url_input"
            )

            fetch_button = st.button(
                "🌐 Fetch Content from URL",
                use_container_width=True,
                disabled=not job_url.strip()
            )

            if fetch_button and job_url.strip():
                st.session_state.fetching_job_url = job_url
                st.session_state.show_job_preview = True
                st.rerun()

            if st.session_state.get("job_url"):
                st.success("✅ Currently using content from URL")
                st.caption(f"Source: {st.session_state.job_url[:50]}...")

                if st.button("🔄 Fetch from Different URL", use_container_width=True):
                    for key in ["fetching_job_url", "show_job_preview"]:
                        st.session_state.pop(key, None)
                    st.rerun()

    st.divider()

    # === Personal Details ===
    with st.expander("✏️ Edit Personal Details"):
        st.markdown("**Update your personal information:**")
        personal_details_input = st.text_area(
            "Personal Details",
            value=st.session_state.personal_details,
            height=300,
        )
        if st.button("💾 Save Personal Details"):
            st.session_state.personal_details = personal_details_input
            show_success_message("Personal details updated!")
            st.rerun()

    st.divider()

    # === Smart RAG System ===
    st.subheader("🧠 Smart RAG System")
    st.markdown(
        "**Semantic Document Search** uses AI to find only relevant document sections."
    )

    use_rag = st.toggle(
        "Enable Smart Document Search (RAG)",
        value=st.session_state.get("use_rag", False),
        key="rag_toggle",
    )
    st.session_state.use_rag = use_rag

    if use_rag:
        try:
            from utils.rag_system import initialize_rag_system, index_documents_if_needed

            rag_system = initialize_rag_system(api_key)
            if st.session_state.documents and not rag_system.chunks:
                with st.spinner("🔄 Indexing documents..."):
                    index_documents_if_needed(rag_system)

            if rag_system.chunks:
                stats = rag_system.get_statistics()
                st.success("✅ RAG System Active")

                col1, col2 = st.columns(2)
                col1.metric("Indexed Chunks", stats["total_chunks"])
                col2.metric("Documents", stats["total_documents"])
                st.metric("Avg Chunk Size", f"{stats['avg_chunk_size']} chars")

                st.caption("📚 Indexed Documents:")
                for src in stats["sources"]:
                    st.text(f"✓ {src}")

                if st.button("🔄 Re-index All Documents", use_container_width=True):
                    rag_system.chunks.clear()
                    rag_system.embeddings_cache.clear()
                    with st.spinner("Re-indexing..."):
                        index_documents_if_needed(rag_system)
                    show_success_message("Documents re-indexed successfully!")
                    st.rerun()
            else:
                st.info("📝 No documents indexed yet. Upload some to enable RAG.")
        except Exception as e:
            st.error(f"❌ Error initializing RAG: {e}")
            st.session_state.use_rag = False
    else:
        st.caption("📄 Standard mode: All documents sent with each request.")

    st.divider()

    # === Portfolio & GitHub ===
    st.subheader("🌐 Portfolio & GitHub")
    portfolio_status = st.session_state.get("portfolio_loaded", False)

    if portfolio_status:
        st.success("✅ Portfolio content loaded")
        col1, col2 = st.columns(2)
        col1.markdown(f"[🌐 Portfolio]({st.session_state.get('portfolio_url', 'N/A')})")
        col2.markdown(f"[💻 GitHub]({st.session_state.get('github_url', 'N/A')})")

        if st.button("🔄 Refresh Portfolio", use_container_width=True):
            from utils.portfolio_fetcher import refresh_portfolio_content

            if refresh_portfolio_content():
                show_success_message("Portfolio refreshed!")
                st.rerun()
    else:
        st.info("📡 Portfolio content not loaded")
        if st.button("📥 Fetch Portfolio & GitHub", use_container_width=True):
            from utils.portfolio_fetcher import load_portfolio_content

            with st.spinner("Fetching content..."):
                if load_portfolio_content():
                    show_success_message("✅ Portfolio and GitHub content loaded!")
                    st.rerun()
                else:
                    st.error("❌ Could not fetch portfolio content. Check internet connection.")

    st.caption("Fetches live content from your portfolio website and GitHub profile.")
    st.divider()

    # === Document Upload Section ===
    st.subheader("📁 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload Resume or Additional Documents",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
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
        for doc_name in list(st.session_state.documents.keys()):
            col1, col2 = st.columns([3, 1])
            col1.text(f"⭐ {doc_name}" if doc_name == RESUME_FILENAME else doc_name)
            if col2.button("🗑️", key=f"delete_{doc_name}"):
                del st.session_state.documents[doc_name]
                st.rerun()

    return api_key
