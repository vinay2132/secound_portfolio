"""
Job Description URL Fetcher
Extracts job descriptions from job posting URLs
"""

import re
from typing import Dict, Optional, List
from dataclasses import dataclass

import streamlit as st

# Optional imports: requests + bs4
try:
    import requests
    from bs4 import BeautifulSoup
    REQUESTS_AVAILABLE = True
except Exception:
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
        if self.session:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.9'
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
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            job_details = JobDetails(url=url)
            job_details.raw_html = response.text

            # Detect job board and use appropriate parser
            if 'linkedin.com' in url:
                job_details = self._parse_linkedin(soup, job_details)
            elif 'indeed.com' in url:
                job_details = self._parse_indeed(soup, job_details)
            elif 'greenhouse.io' in url:
                job_details = self._parse_greenhouse(soup, job_details)
            elif 'lever.co' in url:
                job_details = self._parse_lever(soup, job_details)
            else:
                job_details = self._parse_generic(soup, job_details)

            return job_details

        except Exception as e:
            st.error(f"❌ Error fetching or parsing URL: {str(e)}")
            return None

    def _parse_linkedin(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse LinkedIn job postings"""
        title_elem = soup.find('h1', class_='top-card-layout__title') or soup.find('h1')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)

        company_elem = soup.find('a', class_='topcard__org-name-link') or soup.find('span', class_='topcard__flavor')
        if company_elem:
            job_details.company_name = company_elem.get_text(strip=True)

        location_elem = soup.find('span', class_='topcard__flavor--bullet')
        if location_elem:
            job_details.location = location_elem.get_text(strip=True)

        desc_elem = soup.find('div', class_='description__text') or soup.find('div', class_=re.compile('description', re.I))
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)

        return job_details

    def _parse_indeed(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse Indeed job postings"""
        title_elem = soup.find('h1', class_=re.compile('jobsearch-JobInfoHeader-title', re.I)) or soup.find('h1')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)

        company_elem = soup.find('div', {'data-company-name': True}) or soup.find('div', class_=re.compile('company', re.I))
        if company_elem and company_elem.get('data-company-name'):
            job_details.company_name = company_elem.get('data-company-name')
        elif company_elem:
            job_details.company_name = company_elem.get_text(strip=True)

        location_elem = soup.find('div', {'data-testid': 'job-location'}) or soup.find('div', class_=re.compile('location', re.I))
        if location_elem:
            job_details.location = location_elem.get_text(strip=True)

        desc_elem = soup.find('div', id='jobDescriptionText') or soup.find('div', class_=re.compile('jobDescription', re.I))
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)

        return job_details

    def _parse_greenhouse(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse Greenhouse job postings"""
        title_elem = soup.find('h1', class_='app-title') or soup.find('h1')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)

        company_elem = soup.find('span', class_='company-name') or soup.find('div', class_=re.compile('company', re.I))
        if company_elem:
            job_details.company_name = company_elem.get_text(strip=True)

        location_elem = soup.find('div', class_='location') or soup.find('span', class_=re.compile('location', re.I))
        if location_elem:
            job_details.location = location_elem.get_text(strip=True)

        desc_elem = soup.find('div', id='content') or soup.find('div', class_=re.compile('content', re.I))
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)

        return job_details

    def _parse_lever(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Parse Lever job postings"""
        title_elem = soup.find('h2', class_='posting-headline') or soup.find('h1') or soup.find('h2')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)

        company_elem = soup.find('div', class_='posting-categories') or soup.find('div', class_=re.compile('company', re.I))
        if company_elem:
            texts = [t.strip() for t in company_elem.stripped_strings]
            if texts:
                job_details.company_name = texts[0] if len(texts) > 0 else ""
                job_details.location = texts[1] if len(texts) > 1 else ""

        desc_elem = soup.find('div', class_='content') or soup.find('div', class_=re.compile('content', re.I))
        if desc_elem:
            job_details.description = desc_elem.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)

        return job_details

    def _parse_generic(self, soup: BeautifulSoup, job_details: JobDetails) -> JobDetails:
        """Generic parser for unknown job boards"""
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            job_details.job_title = title_elem.get_text(strip=True)

        company_patterns = [
            soup.find('span', class_=re.compile('company', re.I)),
            soup.find('div', class_=re.compile('company', re.I)),
            soup.find('a', class_=re.compile('company', re.I))
        ]
        for elem in company_patterns:
            if elem:
                job_details.company_name = elem.get_text(strip=True)
                break

        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        if main_content:
            for script in main_content(['script', 'style', 'nav', 'header', 'footer']):
                try:
                    script.decompose()
                except Exception:
                    pass

            job_details.description = main_content.get_text(separator='\n', strip=True)
            self._extract_sections_from_text(job_details)

        return job_details

    def _extract_sections_from_text(self, job_details: JobDetails):
        """Extract structured sections from description text"""
        if not job_details.description:
            return

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
    Universal URL fetcher and display function
    Works with job postings AND general websites

    Args:
        url: Any URL (job posting, career page, company website, etc.)

    Returns:
        JobDetails object if successful, None otherwise
    """
    if not REQUESTS_AVAILABLE:
        st.error("❌ Required packages not installed. Run: pip install requests beautifulsoup4")
        return None

    fetcher = JobURLFetcher()

    with st.spinner(f"🌐 Fetching and analyzing content from URL..."):
        job_details = fetcher.fetch_job_description(url)

    if not job_details:
        return None

    # Check if we got meaningful content
    has_job_info = any([
        bool(job_details.job_title and job_details.job_title.strip()),
        bool(job_details.company_name and job_details.company_name.strip()),
        bool(job_details.responsibilities),
        bool(job_details.qualifications),
        bool(job_details.required_skills)
    ])

    if has_job_info:
        st.success("✅ Job-related content extracted successfully!")
    else:
        st.success("✅ Content extracted successfully!")
        st.info("📝 This appears to be general website content. All available information has been extracted.")

    # Create tabs for different views
    tab1, tab2 = st.tabs(["📋 Structured View", "📄 Full Text"])

    with tab1:
        st.markdown("### Extracted Information")
        st.caption(f"🔗 Source: {url}")

        if has_job_info:
            st.success("🎯 Job posting content detected")
        else:
            st.info("🌐 General website content")

        details_dict = job_details.to_display_dict()

        # Basic Info
        st.markdown("#### 📌 Page Information")
        col1, col2 = st.columns(2)
        with col1:
            for i, (key, value) in enumerate(list(details_dict["Basic Info"].items())[:3]):
                st.markdown(f"**{key}:** {value if value else '*Not found*'}")
        with col2:
            for i, (key, value) in enumerate(list(details_dict["Basic Info"].items())[3:]):
                st.markdown(f"**{key}:** {value if value else '*Not specified*'}")

        st.divider()

        # Main Content/Description
        st.markdown("#### 📝 Main Content")
        with st.container():
            desc_text = details_dict["Description"]
            if len(desc_text) > 1000:
                with st.expander("📄 Click to view full content", expanded=False):
                    st.text_area("Content", desc_text, height=300, disabled=True, key="jd_desc_full")
                st.text_area("Preview (first 1000 characters)", desc_text[:1000] + "...", height=150, disabled=True, key="jd_desc_preview")
            else:
                st.text_area("Content", desc_text, height=200, disabled=True, key="jd_desc")

        st.divider()

        sections_found = False

        # Responsibilities
        if details_dict["Responsibilities"] and details_dict["Responsibilities"] != ["None found"]:
            sections_found = True
            st.markdown(f"#### ✓ Responsibilities ({len(details_dict['Responsibilities'])} items)")
            for i, item in enumerate(details_dict["Responsibilities"][:10], 1):
                st.markdown(f"{i}. {item}")
            if len(details_dict["Responsibilities"]) > 10:
                with st.expander(f"➕ View all {len(details_dict['Responsibilities'])} items"):
                    for i, item in enumerate(details_dict["Responsibilities"], 1):
                        st.markdown(f"{i}. {item}")
            st.divider()

        # Qualifications
        if details_dict["Qualifications"] and details_dict["Qualifications"] != ["None found"]:
            sections_found = True
            st.markdown(f"#### 🎓 Qualifications ({len(details_dict['Qualifications'])} items)")
            for i, item in enumerate(details_dict["Qualifications"][:10], 1):
                st.markdown(f"{i}. {item}")
            if len(details_dict["Qualifications"]) > 10:
                with st.expander(f"➕ View all {len(details_dict['Qualifications'])} items"):
                    for i, item in enumerate(details_dict["Qualifications"], 1):
                        st.markdown(f"{i}. {item}")
            st.divider()

        # Required Skills
        if details_dict["Required Skills"] and details_dict["Required Skills"] != ["None found"]:
            sections_found = True
            st.markdown(f"#### 💻 Required Skills ({len(details_dict['Required Skills'])} items)")
            for i, item in enumerate(details_dict["Required Skills"][:10], 1):
                st.markdown(f"{i}. {item}")
            if len(details_dict["Required Skills"]) > 10:
                with st.expander(f"➕ View all {len(details_dict['Required Skills'])} items"):
                    for i, item in enumerate(details_dict["Required Skills"], 1):
                        st.markdown(f"{i}. {item}")
            st.divider()

        # Preferred Skills
        if details_dict["Preferred Skills"] and details_dict["Preferred Skills"] != ["None found"]:
            sections_found = True
            st.markdown(f"#### ⭐ Preferred Skills ({len(details_dict['Preferred Skills'])} items)")
            for i, item in enumerate(details_dict["Preferred Skills"][:10], 1):
                st.markdown(f"{i}. {item}")
            if len(details_dict["Preferred Skills"]) > 10:
                with st.expander(f"➕ View all {len(details_dict['Preferred Skills'])} items"):
                    for i, item in enumerate(details_dict["Preferred Skills"], 1):
                        st.markdown(f"{i}. {item}")
            st.divider()

        # Benefits
        if details_dict["Benefits"] and details_dict["Benefits"] != ["None found"]:
            sections_found = True
            st.markdown(f"#### 🎁 Benefits ({len(details_dict['Benefits'])} items)")
            for i, item in enumerate(details_dict["Benefits"][:10], 1):
                st.markdown(f"{i}. {item}")
            if len(details_dict["Benefits"]) > 10:
                with st.expander(f"➕ View all {len(details_dict['Benefits'])} items"):
                    for i, item in enumerate(details_dict["Benefits"], 1):
                        st.markdown(f"{i}. {item}")

        if not sections_found:
            st.info("ℹ️ No structured sections detected. All content is shown in the 'Main Content' section above.")

    with tab2:
        st.markdown("### Full Content for AI Processing")
        st.caption("This is the complete text that will be used for AI analysis and matching")

        full_text = job_details.to_formatted_text()

        st.caption(f"📊 Total content: {len(full_text)} characters, ~{len(full_text.split())} words")

        st.text_area("Full Text", full_text, height=500, disabled=True, key="jd_full")

        st.download_button(
            label="📥 Download as Text File",
            data=full_text,
            file_name=f"extracted_content_{job_details.url.split('/')[-1][:20]}.txt",
            mime="text/plain"
        )

    return job_details


def save_job_to_session(job_details: JobDetails):
    """Save fetched job details to session state"""
    st.session_state.job_description = job_details.to_formatted_text()
    st.session_state.jd_configured = True
    st.session_state.job_url = job_details.url
    st.session_state.job_details = job_details
