import re
import datetime
from utils.config import ACTIVITY_FILE
from utils.json_db import read_json, write_json

def validate_email(email):
    """Simple regex for email structure validation."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email.strip()))

def validate_password_strength(password):
    """
    Validates password strength:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one numeric digit
    - At least one special character from: !@#$%^&*()_+-=[]{}|;':",./<>?
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return False, "Password must contain at least one lowercase letter."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one numeric digit."
    if not any(char in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for char in password):
        return False, "Password must contain at least one special character (e.g. !@#$%^&*)."
    return True, "Password is strong."

def log_activity(username, action, details=""):
    """Logs system, authentication, and database modifications into activity.json."""
    activities = read_json(ACTIVITY_FILE)
    if not isinstance(activities, list):
        activities = []
        
    log_entry = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "action": action,
        "details": details
    }
    
    activities.insert(0, log_entry) # Put most recent at the top
    # Cap at 500 entries to prevent files from growing too large
    if len(activities) > 500:
        activities = activities[:500]
        
    write_json(ACTIVITY_FILE, activities)

def setup_page(title):
    """Configures Streamlit page, initializes session state, and injects custom styles."""
    import streamlit as st
    from utils.session import init_session
    from utils.config import ASSETS_DIR
    import os
    
    # 1. Set page config (must be first streamlit call)
    st.set_page_config(
        page_title=f"SmartCampusAI - {title}",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 2. Initialize session variables
    init_session()
    
    # 3. Load and inject custom CSS
    css_path = os.path.join(ASSETS_DIR, "styles.css")
    if os.path.exists(css_path):
        try:
            with open(css_path, "r") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
        except Exception as e:
            print(f"Error loading CSS: {e}")

