"""
Portfolio and GitHub content fetcher
Fetches and processes content from portfolio website and GitHub profile
"""

import streamlit as st
import re
from typing import Dict, Optional
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    st.warning("⚠️ Install 'requests' and 'beautifulsoup4' for portfolio fetching: pip install requests beautifulsoup4")


class PortfolioFetcher:
    """Fetch and process portfolio and GitHub content"""
    
    PORTFOLIO_URL = "https://vinay2132.github.io/my_portfolio/"
    GITHUB_URL = "https://github.com/vinay2132"
    GITHUB_API_URL = "https://api.github.com/users/vinay2132"
    
    def __init__(self):
        self.portfolio_content = None
        self.github_content = None
        self.cached = False
    
    def fetch_portfolio(self) -> Optional[str]:
        """Fetch content from portfolio website"""
        if not REQUESTS_AVAILABLE:
            return None
        
        try:
            response = requests.get(self.PORTFOLIO_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            # Add structured information
            portfolio_data = f"""
=== PORTFOLIO WEBSITE ===
URL: {self.PORTFOLIO_URL}

CONTENT:
{text}

NOTE: This is Vinay Ramesh's personal portfolio website showcasing projects, skills, and contact information.
"""
            self.portfolio_content = portfolio_data
            return portfolio_data
            
        except Exception as e:
            st.warning(f"Could not fetch portfolio: {str(e)}")
            return None
    
    def fetch_github_profile(self) -> Optional[str]:
        """Fetch GitHub profile information"""
        if not REQUESTS_AVAILABLE:
            return None
        
        try:
            # Fetch GitHub API data
            response = requests.get(self.GITHUB_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Fetch repositories
            repos_url = data.get('repos_url')
            repos_response = requests.get(repos_url, timeout=10)
            repos = repos_response.json() if repos_response.status_code == 200 else []
            
            # Build structured content
            github_data = f"""
=== GITHUB PROFILE ===
URL: {self.GITHUB_URL}
Profile: {data.get('html_url', self.GITHUB_URL)}

PROFILE INFORMATION:
- Username: {data.get('login', 'vinay2132')}
- Name: {data.get('name', 'Vinay Ramesh')}
- Bio: {data.get('bio', 'Full Stack Developer')}
- Public Repositories: {data.get('public_repos', 'Multiple')}
- Followers: {data.get('followers', 0)}
- Following: {data.get('following', 0)}
- Location: {data.get('location', 'Denton, TX')}
- Company: {data.get('company', 'N/A')}

TOP REPOSITORIES:
"""
            # Add top repositories (sorted by stars)
            repos_sorted = sorted(repos, key=lambda x: x.get('stargazers_count', 0), reverse=True)
            for idx, repo in enumerate(repos_sorted[:10], 1):
                github_data += f"""
{idx}. {repo.get('name', 'Unknown')}
   - Description: {repo.get('description', 'No description')}
   - Language: {repo.get('language', 'N/A')}
   - Stars: {repo.get('stargazers_count', 0)}
   - URL: {repo.get('html_url', '')}
"""
            
            github_data += f"""

NOTE: Visit {self.GITHUB_URL} for complete list of projects and contributions.
"""
            
            self.github_content = github_data
            return github_data
            
        except Exception as e:
            st.warning(f"Could not fetch GitHub profile: {str(e)}")
            return None
    
    def fetch_all(self) -> Dict[str, str]:
        """Fetch all portfolio and GitHub content"""
        results = {}
        
        with st.spinner("🌐 Fetching portfolio and GitHub content..."):
            portfolio = self.fetch_portfolio()
            if portfolio:
                results['portfolio_content.txt'] = portfolio
            
            github = self.fetch_github_profile()
            if github:
                results['github_profile.txt'] = github
        
        self.cached = True
        return results
    
    def get_links_context(self) -> str:
        """Get formatted links for including in communications"""
        return f"""
MY ONLINE PRESENCE:
- Portfolio Website: {self.PORTFOLIO_URL}
- GitHub Profile: {self.GITHUB_URL}
- LinkedIn: [Add if available]

You can explore my projects and code samples at the above links.
"""
    
    @staticmethod
    def extract_projects_from_github(github_content: str) -> list:
        """Extract project information from GitHub content"""
        projects = []
        if not github_content:
            return projects
        
        # Simple regex to extract repository info
        repo_pattern = r'\d+\.\s+(.+?)\n\s+-\s+Description:\s+(.+?)\n\s+-\s+Language:\s+(.+?)\n\s+-\s+Stars:\s+(\d+)\n\s+-\s+URL:\s+(.+?)(?:\n|$)'
        matches = re.findall(repo_pattern, github_content, re.MULTILINE)
        
        for match in matches:
            projects.append({
                'name': match[0].strip(),
                'description': match[1].strip(),
                'language': match[2].strip(),
                'stars': int(match[3]),
                'url': match[4].strip()
            })
        
        return projects


def load_portfolio_content() -> bool:
    """Load portfolio and GitHub content into session state"""
    if 'portfolio_loaded' in st.session_state and st.session_state.portfolio_loaded:
        return True
    
    fetcher = PortfolioFetcher()
    content = fetcher.fetch_all()
    
    if content:
        # Add to documents
        for filename, text in content.items():
            st.session_state.documents[filename] = text
        
        # Store links
        st.session_state.portfolio_links = fetcher.get_links_context()
        st.session_state.portfolio_url = fetcher.PORTFOLIO_URL
        st.session_state.github_url = fetcher.GITHUB_URL
        st.session_state.portfolio_loaded = True
        
        return True
    
    return False


def refresh_portfolio_content() -> bool:
    """Refresh portfolio content from web"""
    # Remove old content
    if 'portfolio_content.txt' in st.session_state.documents:
        del st.session_state.documents['portfolio_content.txt']
    if 'github_profile.txt' in st.session_state.documents:
        del st.session_state.documents['github_profile.txt']
    
    st.session_state.portfolio_loaded = False
    
    return load_portfolio_content()


def get_portfolio_links_for_email() -> str:
    """Get formatted portfolio links for email signature"""
    portfolio_url = st.session_state.get('portfolio_url', 'https://vinay2132.github.io/my_portfolio/')
    github_url = st.session_state.get('github_url', 'https://github.com/vinay2132')
    
    return f"""
🌐 Portfolio: {portfolio_url}
💻 GitHub: {github_url}
"""