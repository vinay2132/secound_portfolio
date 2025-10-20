"""
Job Description URL Fetcher
Extracts job descriptions from job posting URLs
"""

import streamlit as st
import re
from typing import Dict, Optional, List
from dataclasses import dataclass
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


@dataclass
class JobDetails:
    """Structured job details extracted from URL"""
    job_title: str = ""
    company_name: str = ""
    location: str = ""
    job_type: str = ""
    salary_range: str = ""
    description: str = ""
    responsibilities: List[str] = None
    qualifications: List[str] = None
    required_skills: List[str] = None
    preferred_skills: List[str] = None
    benefits: List[str] = None
    raw_html: str = ""
    url: str = ""
    
    def __post_init__(self):
        if self.responsibilities is None:
            self.responsibilities = []
        if self.qualifications is None:
            self.qualifications = []
        if self.required_skills is None:
            self.required_skills = []
        if self.preferred_skills is None:
            self.preferred_skills = []
        if self.benefits is None:
            self.benefits = []
    
    def to_formatted_text(self) -> str:
        """Convert to formatted text for display and AI processing"""
        text = f"""
JOB POSTING DETAILS
{'='*60}

SOURCE URL: {self.url}

BASIC INFORMATION:
- Job Title: {self.job_title or 'Not found'}
- Company: {self.company_name or 'Not found'}
- Location: {self.location or 'Not found'}
- Job Type: {self.job_type or 'Not found'}
- Salary Range: {self.salary_range or 'Not specified'}

JOB DESCRIPTION:
{self.description or 'No description available'}

"""
        
        if self.responsibilities:
            text += "RESPONSIBILITIES:\n"
            for i, resp in enumerate(self.responsibilities, 1):
                text += f"{i}. {resp}\n"
            text += "\n"
        
        if self.qualifications:
            text += "QUALIFICATIONS:\n"
            for i, qual in enumerate(self.qualifications, 1):
                text += f"{i}. {qual}\n"
            text += "\n"
        
        if self.required_skills:
            text += "REQUIRED SKILLS:\n"
            for i, skill in enumerate(self.required_skills, 1):
                text += f"{i}. {skill}\n"
            text += "\n"
        
        if self.preferred_skills:
            text += "PREFERRED SKILLS:\n"
            for i, skill in enumerate(self.preferred_skills, 1):
                text += f"{i}. {skill}\n"
            text += "\n"
        
        if self.benefits:
            text += "BENEFITS:\n"
            for i, benefit in enumerate(self.benefits, 1):
                text += f"{i}. {benefit}\n"
            text += "\n"
        
        return text
    
    def to_display_dict(self) -> Dict:
        """Convert to dictionary for structured display"""
        return {
            "Basic Info": {
                "Job Title": self.job_title or "Not found",
                "Company": self.company_name or "Not found",
                "Location": self.location or "Not found",
                "Job Type": self.job_type or "Not found",
                "Salary": self.salary_range or "Not specified"
            },
            "Description": self.description or "No description available",
            "Responsibilities": self.responsibilities if self.responsibilities else ["None found"],
            "Qualifications": self.qualifications if self.qualifications else ["None found"],
            "Required Skills": self.required_skills if self.required_skills else ["None found"],
            "Preferred Skills": self.preferred_skills if self.preferred_skills else ["None found"],
            "Benefits": self.benefits if self.benefits else ["None found"]
        }


class JobURLFetcher:
    """Fetch and parse job descriptions from various job board URLs"""
    
    SUPPORTED_SITES = {
        'linkedin.com': 'LinkedIn',
        'indeed.com': 'Indeed',
        'glassdoor.com': 'Glassdoor',
        'monster.com': 'Monster',
        'careerbuilder.com': 'CareerBuilder',
        'ziprecruiter.com': 'ZipRecruiter',
        'dice.com': 'Dice',
        'greenhouse.io': 'Greenhouse',
        'lever.co': 'Lever',
        'workday.com': 'Workday'
    }
    
    def __init__(self):
        self.session = requests.Session() if REQUESTS_AVAILABLE else None
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_job_description(self, url: str) -> Optional[JobDetails]:
        """
        Fetch and parse job description from URL
        
        Args:
            url: Job posting URL
            
        Returns:
            JobDetails object with extracted information
        """
        if not REQUESTS_AVAILABLE:
            st.error("❌ Please install required packages: pip install requests beautifulsoup4")
            return None
        
        try:
            # Fetch the page
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Detect job board and use appropriate parser
            job_details = JobDetails(url=url)
            job_details.raw_html = response.text
            
            # Try different parsing strategies
            if 'linkedin.com' in url:
                job_details = self._parse_linkedin(soup, job_details)
            elif 'indeed.com' in url:
                job_details = self._parse_indeed(soup, job_details)
            elif 'greenhouse.io' in url:
                job_details = self._parse_greenhouse(soup, job_details)
            elif 'lever.co' in url:
                job_details = self._parse_lever(soup, job_details)
            else:
                # Generic parser for other sites
                job_details = self._parse_generic(soup, job_details)
            
            return job_details
            
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error fetching URL: {str(e)}")
            return None
        except Exception as e:
            st.error(f"❌ Error parsing job description: {str(e)}")
            return None
    
    def _parse_linkedin(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse LinkedIn job postings"""
        # Job title
        title_elem = soup.find('h1', class_='top-card-layout__title') or soup.find('h1')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)
        
        # Company name
        company_elem = soup.find('a', class_='topcard__org-name-link') or soup.find('span', class_='topcard__flavor')
        if company_elem:
            job_details.company_name = company_elem.get_text(strip=True)
        
        # Location
        location_elem = soup.find('span', class_='topcard__flavor--bullet')
        if location_elem:
            job_details.location = location_elem.get_text(strip=True)
        
        # Description
        desc_elem = soup.find('div', class_='description__text')
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)
        
        return job_details
    
    def _parse_indeed(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse Indeed job postings"""
        # Job title
        title_elem = soup.find('h1', class_='jobsearch-JobInfoHeader-title')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)
        
        # Company name
        company_elem = soup.find('div', {'data-company-name': True})
        if company_elem:
            job_details.company_name = company_elem.get('data-company-name')
        
        # Location
        location_elem = soup.find('div', {'data-testid': 'job-location'})
        if location_elem:
            job_details.location = location_elem.get_text(strip=True)
        
        # Description
        desc_elem = soup.find('div', id='jobDescriptionText')
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)
        
        return job_details
    
    def _parse_greenhouse(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse Greenhouse job postings"""
        # Job title
        title_elem = soup.find('h1', class_='app-title')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)
        
        # Company name
        company_elem = soup.find('span', class_='company-name')
        if company_elem:
            job_details.company_name = company_elem.get_text(strip=True)
        
        # Location
        location_elem = soup.find('div', class_='location')
        if location_elem:
            job_details.location = location_elem.get_text(strip=True)
        
        # Description
        desc_elem = soup.find('div', id='content')
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)
        
        return job_details
    
    def _parse_lever(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse Lever job postings"""
        # Job title
        title_elem = soup.find('h2', class_='posting-headline')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)
        
        # Company name and location often in same div
        company_elem = soup.find('div', class_='posting-categories')
        if company_elem:
            texts = [t.strip() for t in company_elem.stripped_strings]
            if texts:
                job_details.company_name = texts[0] if len(texts) > 0 else ""
                job_details.location = texts[1] if len(texts) > 1 else ""
        
        # Description
        desc_elem = soup.find('div', class_='content')
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)
        
        return job_details
    
    def _parse_generic(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Generic parser for unknown job boards"""
        # Try to find job title (usually in h1 or title)
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)
        
        # Try to find company name (common patterns)
        company_patterns = [
            soup.find('span', class_=re.compile('company', re.I)),
            soup.find('div', class_=re.compile('company', re.I)),
            soup.find('a', class_=re.compile('company', re.I))
        ]
        for elem in company_patterns:
            if elem:
                job_details.company_name = elem.get_text(strip=True)
                break
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if main_content:
            # Remove script and style elements
            for script in main_content(['script', 'style', 'nav', 'header', 'footer']):
                script.decompose()
            
            job_details.description = main_content.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)
        
        return job_details
    
    def _extract_sections_from_text(self, job_details: JobDetails):
        """Extract structured sections from description text"""
        text = job_details.description.lower()
        lines = job_details.description.split('\n')
        
        current_section = None
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Detect section headers
            if any(keyword in line_lower for keyword in ['responsibilities', 'duties', 'you will']):
                current_section = 'responsibilities'
                continue
            elif any(keyword in line_lower for keyword in ['qualifications', 'requirements', 'must have']):
                current_section = 'qualifications'
                continue
            elif any(keyword in line_lower for keyword in ['required skills', 'technical skills', 'must know']):
                current_section = 'required_skills'
                continue
            elif any(keyword in line_lower for keyword in ['preferred', 'nice to have', 'bonus']):
                current_section = 'preferred_skills'
                continue
            elif any(keyword in line_lower for keyword in ['benefits', 'we offer', 'perks']):
                current_section = 'benefits'
                continue
            
            # Add to current section if we're in one
            if current_section and line.strip() and len(line.strip()) > 10:
                # Clean bullet points
                cleaned_line = re.sub(r'^[\s\-\*•●]+', '', line).strip()
                if cleaned_line:
                    if current_section == 'responsibilities':
                        job_details.responsibilities.append(cleaned_line)
                    elif current_section == 'qualifications':
                        job_details.qualifications.append(cleaned_line)
                    elif current_section == 'required_skills':
                        job_details.required_skills.append(cleaned_line)
                    elif current_section == 'preferred_skills':
                        job_details.preferred_skills.append(cleaned_line)
                    elif current_section == 'benefits':
                        job_details.benefits.append(cleaned_line)


def fetch_and_display_job(url: str) -> Optional[JobDetails]:
    """
    Fetch job description from URL and display structured information
    
    Args:
        url: Job posting URL
        
    Returns:
        JobDetails object if successful, None otherwise
    """
    if not REQUESTS_AVAILABLE:
        st.error("❌ Required packages not installed. Run: pip install requests beautifulsoup4")
        return None
    
    fetcher = JobURLFetcher()
    
    with st.spinner(f"🌐 Fetching job description from URL..."):
        job_details = fetcher.fetch_job_description(url)
    
    if not job_details:
        return None
    
    # Display structured information
    st.success("✅ Job description fetched successfully!")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📋 Structured View", "📄 Full Text"])
    
    with tab1:
        st.markdown("### Extracted Job Details")
        st.caption("Review and verify the extracted information below")
        
        details_dict = job_details.to_display_dict()
        
        # Basic Info - Display directly without nested expander
        st.markdown("#### 📌 Basic Information")
        for key, value in details_dict["Basic Info"].items():
            st.markdown(f"**{key}:** {value}")
        
        st.divider()
        
        # Description
        st.markdown("#### 📝 Job Description")
        with st.container():
            st.text_area("Description", details_dict["Description"], height=150, disabled=True, key="jd_desc")
        
        st.divider()
        
        # Responsibilities
        if details_dict["Responsibilities"] != ["None found"]:
            st.markdown(f"#### ✓ Responsibilities ({len(details_dict['Responsibilities'])} items)")
            for i, item in enumerate(details_dict["Responsibilities"], 1):
                st.markdown(f"{i}. {item}")
            st.divider()
        
        # Qualifications
        if details_dict["Qualifications"] != ["None found"]:
            st.markdown(f"#### 🎓 Qualifications ({len(details_dict['Qualifications'])} items)")
            for i, item in enumerate(details_dict["Qualifications"], 1):
                st.markdown(f"{i}. {item}")
            st.divider()
        
        # Required Skills
        if details_dict["Required Skills"] != ["None found"]:
            st.markdown(f"#### 💻 Required Skills ({len(details_dict['Required Skills'])} items)")
            for i, item in enumerate(details_dict["Required Skills"], 1):
                st.markdown(f"{i}. {item}")
            st.divider()
        
        # Preferred Skills
        if details_dict["Preferred Skills"] != ["None found"]:
            st.markdown(f"#### ⭐ Preferred Skills ({len(details_dict['Preferred Skills'])} items)")
            for i, item in enumerate(details_dict["Preferred Skills"], 1):
                st.markdown(f"{i}. {item}")
            st.divider()
        
        # Benefits
        if details_dict["Benefits"] != ["None found"]:
            st.markdown(f"#### 🎁 Benefits ({len(details_dict['Benefits'])} items)")
            for i, item in enumerate(details_dict["Benefits"], 1):
                st.markdown(f"{i}. {item}")
    
    with tab2:
        st.markdown("### Full Job Description Text")
        st.caption("This is the complete text that will be used for AI processing")
        st.text_area("Full Text", job_details.to_formatted_text(), height=400, disabled=True, key="jd_full")
    
    return job_details


def save_job_to_session(job_details: JobDetails):
    """Save fetched job details to session state"""
    st.session_state.job_description = job_details.to_formatted_text()
    st.session_state.jd_configured = True
    st.session_state.job_url = job_details.url
    st.session_state.job_details = job_details