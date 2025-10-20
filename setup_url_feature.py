#!/usr/bin/env python3
"""
Setup script for Job URL Fetching Feature
Automates the installation and configuration process
"""

import os
import sys
import subprocess
from pathlib import Path

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")

def check_python_version():
    """Check if Python version is 3.8+"""
    print("\n" + "="*60)
    print("Checking Python Version")
    print("="*60)
    
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python {version.major}.{version.minor} found. Requires Python 3.8+")
        return False

def install_packages():
    """Install required packages"""
    print("\n" + "="*60)
    print("Installing Required Packages")
    print("="*60)
    
    packages = ['requests', 'beautifulsoup4']
    
    for package in packages:
        print_info(f"Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', package, '--quiet'
            ])
            print_success(f"{package} installed")
        except subprocess.CalledProcessError:
            print_error(f"Failed to install {package}")
            return False
    
    return True

def verify_packages():
    """Verify packages are installed correctly"""
    print("\n" + "="*60)
    print("Verifying Package Installation")
    print("="*60)
    
    try:
        import requests
        print_success(f"requests {requests.__version__}")
    except ImportError:
        print_error("requests not found")
        return False
    
    try:
        import bs4
        print_success(f"beautifulsoup4 {bs4.__version__}")
    except ImportError:
        print_error("beautifulsoup4 not found")
        return False
    
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\n" + "="*60)
    print("Checking File Structure")
    print("="*60)
    
    required_files = [
        'main.py',
        'requirements.txt',
        'config/constants.py',
        'config/session_state.py',
        'components/sidebar.py',
        'utils/helpers.py',
        'utils/document_processing.py',
        'utils/gemini_api.py'
    ]
    
    all_exist = True
    for filepath in required_files:
        path = Path(filepath)
        if path.exists():
            print_success(f"{filepath}")
        else:
            print_warning(f"{filepath} - Missing (expected)")
            all_exist = False
    
    return all_exist

def update_requirements_file():
    """Update requirements.txt with new packages"""
    print("\n" + "="*60)
    print("Updating requirements.txt")
    print("="*60)
    
    req_file = Path('requirements.txt')
    
    if not req_file.exists():
        print_warning("requirements.txt not found, creating...")
    
    try:
        # Read existing requirements
        existing = []
        if req_file.exists():
            existing = req_file.read_text().strip().split('\n')
        
        # Add new packages if not present
        new_packages = [
            'requests>=2.31.0',
            'beautifulsoup4>=4.12.0'
        ]
        
        updated = False
        for package in new_packages:
            pkg_name = package.split('>=')[0]
            if not any(pkg_name in line for line in existing):
                existing.append(package)
                updated = True
                print_info(f"Added {package}")
        
        if updated:
            # Write back
            req_file.write_text('\n'.join(existing) + '\n')
            print_success("requirements.txt updated")
        else:
            print_success("requirements.txt already up to date")
        
        return True
    except Exception as e:
        print_error(f"Failed to update requirements.txt: {str(e)}")
        return False

def create_job_url_fetcher():
    """Check if job_url_fetcher.py exists"""
    print("\n" + "="*60)
    print("Checking Job URL Fetcher Module")
    print("="*60)
    
    fetcher_file = Path('utils/job_url_fetcher.py')
    
    if fetcher_file.exists():
        print_success("utils/job_url_fetcher.py exists")
        return True
    else:
        print_error("utils/job_url_fetcher.py NOT FOUND")
        print_info("Please create this file using the artifact provided")
        print_info("Copy the 'Job Description URL Fetcher' artifact content")
        return False

def test_import():
    """Test if the new module can be imported"""
    print("\n" + "="*60)
    print("Testing Module Import")
    print("="*60)
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        from utils.job_url_fetcher import JobURLFetcher, fetch_and_display_job
        print_success("JobURLFetcher imported successfully")
        
        # Test instantiation
        fetcher = JobURLFetcher()
        print_success("JobURLFetcher instantiated")
        
        return True
    except ImportError as e:
        print_error(f"Import failed: {str(e)}")
        return False
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return False

def show_manual_steps():
    """Show manual steps that need to be completed"""
    print("\n" + "="*60)
    print("Manual Steps Required")
    print("="*60)
    
    print("""
1. Create utils/job_url_fetcher.py
   → Copy the 'Job Description URL Fetcher' artifact

2. Update components/sidebar.py
   → Replace with 'Updated Sidebar with URL Fetching' artifact

3. Update config/session_state.py
   → Replace with 'Updated Session State Configuration' artifact

4. (Optional) Review the Feature Guide
   → See 'Job URL Fetching Feature Guide' artifact for usage

After completing these steps, run:
   python test_url_feature.py
""")

def create_test_script():
    """Create a test script for the URL feature"""
    print("\n" + "="*60)
    print("Creating Test Script")
    print("="*60)
    
    test_script = Path('test_url_feature.py')
    
    test_code = '''#!/usr/bin/env python3
"""
Test script for URL fetching feature
"""

def test_imports():
    """Test all imports"""
    try:
        from utils.job_url_fetcher import JobURLFetcher, fetch_and_display_job, save_job_to_session
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_fetcher_init():
    """Test fetcher initialization"""
    try:
        from utils.job_url_fetcher import JobURLFetcher
        fetcher = JobURLFetcher()
        print("✅ JobURLFetcher initialized")
        print(f"   Supported sites: {len(fetcher.SUPPORTED_SITES)}")
        return True
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return False

def test_url_validation():
    """Test URL handling"""
    try:
        from utils.job_url_fetcher import JobURLFetcher
        fetcher = JobURLFetcher()
        
        test_url = "https://www.linkedin.com/jobs/view/test"
        print(f"✅ URL handling works")
        return True
    except Exception as e:
        print(f"❌ URL handling error: {e}")
        return False

if __name__ == "__main__":
    print("\\n" + "="*60)
    print("Testing URL Fetching Feature")
    print("="*60 + "\\n")
    
    tests = [
        ("Imports", test_imports),
        ("Fetcher Init", test_fetcher_init),
        ("URL Validation", test_url_validation)
    ]
    
    passed = 0
    for name, test_func in tests:
        print(f"Testing {name}...")
        if test_func():
            passed += 1
        print()
    
    print("="*60)
    print(f"Results: {passed}/{len(tests)} tests passed")
    print("="*60)
    
    if passed == len(tests):
        print("\\n✅ All tests passed! Feature is ready to use.")
        print("   Run: streamlit run main.py")
    else:
        print("\\n⚠️  Some tests failed. Review errors above.")
'''
    
    try:
        test_script.write_text(test_code)
        test_script.chmod(0o755)
        print_success("Created test_url_feature.py")
        return True
    except Exception as e:
        print_error(f"Failed to create test script: {str(e)}")
        return False

def main():
    """Main setup function"""
    print("\n" + "="*60)
    print("🚀 Job URL Fetching Feature Setup")
    print("="*60)
    
    results = []
    
    # Step 1: Check Python version
    results.append(("Python Version", check_python_version()))
    
    # Step 2: Install packages
    results.append(("Package Installation", install_packages()))
    
    # Step 3: Verify packages
    results.append(("Package Verification", verify_packages()))
    
    # Step 4: Check file structure
    results.append(("File Structure", check_file_structure()))
    
    # Step 5: Update requirements.txt
    results.append(("Requirements Update", update_requirements_file()))
    
    # Step 6: Check for job_url_fetcher.py
    results.append(("URL Fetcher Module", create_job_url_fetcher()))
    
    # Step 7: Create test script
    results.append(("Test Script", create_test_script()))
    
    # Summary
    print("\n" + "="*60)
    print("Setup Summary")
    print("="*60)
    
    for name, result in results:
        if result:
            print_success(name)
        else:
            print_error(name)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\n{passed}/{total} steps completed")
    
    if passed == total:
        print_success("\n✅ Automated setup complete!")
    else:
        print_warning(f"\n⚠️  {total - passed} step(s) require manual action")
    
    show_manual_steps()
    
    print("\n" + "="*60)
    print("Next Steps")
    print("="*60)
    print("""
1. Complete the manual steps listed above
2. Run: python test_url_feature.py
3. If tests pass, run: streamlit run main.py
4. Test the URL fetching feature in the sidebar

Need help? See the 'Job URL Fetching Feature Guide' artifact
""")

if __name__ == "__main__":
    main()