"""
Enhanced RAG (Retrieval-Augmented Generation) Implementation
Adds semantic search and intelligent document chunking
"""

import streamlit as st
import google.generativeai as genai
from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass
import re


@dataclass
class DocumentChunk:
    """Represents a chunk of document with metadata"""
    content: str
    source: str
    chunk_id: int
    embedding: np.ndarray = None
    metadata: Dict = None


class EnhancedRAGSystem:
    """
    Enhanced RAG system with semantic search capabilities
    Uses Gemini's embedding API for semantic matching
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.chunks: List[DocumentChunk] = []
        self.embeddings_cache = {}
        
    def chunk_document(self, text: str, source: str, chunk_size: int = 1000, 
                       overlap: int = 200) -> List[DocumentChunk]:
        """
        Split document into overlapping chunks for better context preservation
        
        Args:
            text: Document text
            source: Document name/source
            chunk_size: Target size of each chunk in characters
            overlap: Overlap between chunks to maintain context
        """
        # Clean text
        text = re.sub(r'\s+', ' ', text).strip()
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence endings
                sentence_end = max(
                    text.rfind('.', start, end),
                    text.rfind('!', start, end),
                    text.rfind('?', start, end),
                    text.rfind('\n', start, end)
                )
                if sentence_end > start:
                    end = sentence_end + 1
            
            chunk_text = text[start:end].strip()
            
            if chunk_text:
                chunks.append(DocumentChunk(
                    content=chunk_text,
                    source=source,
                    chunk_id=chunk_id,
                    metadata={'start_pos': start, 'end_pos': end}
                ))
                chunk_id += 1
            
            start = end - overlap
        
        return chunks
    
    def get_embedding(self, text: str) -> np.ndarray:
        """
        Get embedding vector for text using Gemini API
        Implements caching to reduce API calls
        """
        # Check cache first
        text_hash = hash(text[:500])  # Hash first 500 chars for cache key
        if text_hash in self.embeddings_cache:
            return self.embeddings_cache[text_hash]
        
        try:
            # Use Gemini embedding model
            result = genai.embed_content(
                model="models/embedding-001",
                content=text,
                task_type="retrieval_document"
            )
            embedding = np.array(result['embedding'])
            
            # Cache the result
            self.embeddings_cache[text_hash] = embedding
            return embedding
            
        except Exception as e:
            st.warning(f"Embedding error: {e}. Using fallback.")
            # Fallback: simple hash-based pseudo-embedding
            return np.random.rand(768)  # Standard embedding dimension
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def index_documents(self, documents: Dict[str, str], chunk_size: int = 1000):
        """
        Process and index all documents
        
        Args:
            documents: Dict of {filename: content}
            chunk_size: Size of text chunks
        """
        self.chunks = []
        
        with st.spinner("📚 Indexing documents with semantic search..."):
            progress_bar = st.progress(0)
            total_docs = len(documents)
            
            for idx, (source, content) in enumerate(documents.items()):
                # Chunk the document
                doc_chunks = self.chunk_document(content, source, chunk_size)
                
                # Generate embeddings for each chunk
                for chunk in doc_chunks:
                    chunk.embedding = self.get_embedding(chunk.content)
                
                self.chunks.extend(doc_chunks)
                progress_bar.progress((idx + 1) / total_docs)
            
            progress_bar.empty()
            st.success(f"✅ Indexed {len(self.chunks)} chunks from {total_docs} documents")
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[DocumentChunk]:
        """
        Retrieve most relevant chunks for a query using semantic search
        
        Args:
            query: User query or context
            top_k: Number of top chunks to retrieve
        """
        if not self.chunks:
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for chunk in self.chunks:
            if chunk.embedding is not None:
                sim = self.cosine_similarity(query_embedding, chunk.embedding)
                similarities.append((sim, chunk))
        
        # Sort by similarity and return top_k
        similarities.sort(reverse=True, key=lambda x: x[0])
        
        return [chunk for _, chunk in similarities[:top_k]]
    
    def build_context(self, query: str, base_context: str, 
                     max_chunks: int = 5) -> str:
        """
        Build enhanced context using RAG
        
        Args:
            query: User query
            base_context: Basic context (guidelines, personal details)
            max_chunks: Maximum number of relevant chunks to include
        """
        # Retrieve relevant chunks
        relevant_chunks = self.retrieve_relevant_chunks(query, top_k=max_chunks)
        
        # Build context
        context = f"""{base_context}

RELEVANT INFORMATION FROM YOUR DOCUMENTS:
"""
        
        seen_sources = set()
        for chunk in relevant_chunks:
            if chunk.source not in seen_sources:
                context += f"\n--- From {chunk.source} ---\n"
                seen_sources.add(chunk.source)
            context += f"{chunk.content}\n\n"
        
        return context
    
    def generate_with_rag(self, prompt_template: str, query_context: str, 
                         model_name: str = "gemini-2.0-flash-exp", **kwargs) -> str:
        """
        Generate content using RAG-enhanced context
        
        Args:
            prompt_template: Prompt template with placeholders
            query_context: Context about what user is asking for
            model_name: Gemini model to use
            **kwargs: Variables to fill in prompt template
        """
        # Get base context (guidelines, personal details, job description)
        base_context = self._get_base_context()
        
        # Build enhanced context with relevant chunks
        enhanced_context = self.build_context(query_context, base_context)
        
        # Fill template
        filled_prompt = prompt_template.format(**kwargs)
        
        # Combine and generate
        full_prompt = f"{enhanced_context}\n\n{filled_prompt}"
        
        try:
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
    
    def _get_base_context(self) -> str:
        """Get base context from session state"""
        return f"""{st.session_state.writing_guidelines}

PERSONAL DETAILS:
{st.session_state.personal_details}

TARGET JOB DESCRIPTION:
{st.session_state.job_description}
"""
    
    def get_statistics(self) -> Dict:
        """Get statistics about indexed documents"""
        if not self.chunks:
            return {
                'total_chunks': 0,
                'total_documents': 0,
                'avg_chunk_size': 0
            }
        
        sources = set(chunk.source for chunk in self.chunks)
        avg_size = sum(len(chunk.content) for chunk in self.chunks) / len(self.chunks)
        
        return {
            'total_chunks': len(self.chunks),
            'total_documents': len(sources),
            'avg_chunk_size': int(avg_size),
            'sources': list(sources)
        }


# Integration helper functions

def initialize_rag_system(api_key: str) -> EnhancedRAGSystem:
    """Initialize RAG system and store in session state"""
    if 'rag_system' not in st.session_state:
        st.session_state.rag_system = EnhancedRAGSystem(api_key)
    return st.session_state.rag_system


def index_documents_if_needed(rag_system: EnhancedRAGSystem):
    """Index documents if not already indexed"""
    if not rag_system.chunks and st.session_state.documents:
        rag_system.index_documents(st.session_state.documents)


def generate_email_with_rag(rag_system: EnhancedRAGSystem, 
                            email_purpose: str, 
                            email_tone: str,
                            salutation: str,
                            additional_context: str) -> str:
    """
    Generate email using RAG system
    Example integration with email writer
    """
    query_context = f"""
    Generate a {email_tone} {email_purpose} email.
    Focus on: job requirements, matching skills, relevant projects.
    Additional context: {additional_context}
    """
    
    prompt_template = """
TASK: Write a {email_tone} job application email for: {email_purpose}

SALUTATION: {salutation}

ADDITIONAL CONTEXT:
{additional_context}

REQUIREMENTS:
- Start with: Subject: [create a short, relevant subject line]
- Use the salutation: {salutation}
- Keep it to 1-2 SHORT paragraphs maximum
- Highlight specific technologies that match the job and my background
- Reference relevant projects that demonstrate required skills
- Mention F1 OPT work authorization
- End with proper signature
- Make it sound human and confident
- NO bold text or excessive formatting

Generate the email now:
"""
    
    return rag_system.generate_with_rag(
        prompt_template,
        query_context,
        email_tone=email_tone,
        email_purpose=email_purpose,
        salutation=salutation,
        additional_context=additional_context
    )


# Example usage in Streamlit component
def render_rag_status():
    """Render RAG system status in sidebar"""
    if 'rag_system' in st.session_state:
        rag = st.session_state.rag_system
        stats = rag.get_statistics()
        
        with st.expander("🧠 Smart RAG System Status"):
            if stats['total_chunks'] > 0:
                st.success(f"✅ RAG System Active")
                st.metric("Indexed Chunks", stats['total_chunks'])
                st.metric("Documents", stats['total_documents'])
                st.metric("Avg Chunk Size", f"{stats['avg_chunk_size']} chars")
                
                st.markdown("**Indexed Documents:**")
                for source in stats['sources']:
                    st.text(f"  • {source}")
            else:
                st.info("📝 No documents indexed yet")
                if st.button("🔄 Index Documents Now"):
                    index_documents_if_needed(rag)
                    st.rerun()