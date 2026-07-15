import streamlit as st
from utils.helper import setup_page, log_activity
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import SETTINGS_FILE, ANNOUNCEMENTS_FILE
from utils.json_db import read_json, write_json
import datetime

# 1. Initialize Page Config & Styles
setup_page("Settings")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>Global Settings & Tools</h2>", unsafe_allow_html=True)

# Roles checking
user_role = st.session_state.get("role", "Student")
is_admin = user_role == "Admin"

settings = read_json(SETTINGS_FILE)
if not isinstance(settings, dict):
    settings = {"theme": "dark"}

# Section 1: Dashboard Preferences
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h3>⚙️ Preferences</h3>", unsafe_allow_html=True)

with st.form("form_preferences"):
    theme_opt = st.selectbox("Dashboard Base Theme", ["Dark Mode", "Light Mode"], index=0 if settings.get("theme", "dark") == "dark" else 1)
    academic_year = st.selectbox("Default Academic Calendar", ["2025-2026", "2026-2027"], index=0)
    ai_status = st.toggle("Enable OpenAI Agent Assistance", value=settings.get("ai_enabled", True))
    
    submit_pref = st.form_submit_button("Save Preferences")
    
    if submit_pref:
        settings["theme"] = "dark" if theme_opt == "Dark Mode" else "light"
        settings["academic_year"] = academic_year
        settings["ai_enabled"] = ai_status
        
        if write_json(SETTINGS_FILE, settings):
            st.session_state.theme = settings["theme"]
            st.success("Platform configurations saved!")
            log_activity(st.session_state.username, "Update Settings", f"Theme: {settings['theme']}, AI: {ai_status}")
            st.rerun()
        else:
            st.error("Failed to save configuration.")
st.markdown("</div>", unsafe_allow_html=True)

# Section 2: Create Announcements (Admin only)
if is_admin:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📣 Publish Announcement</h3>", unsafe_allow_html=True)
    st.write("Post news or alerts that will display on the main dashboard for all campus members.")
    
    with st.form("form_create_announcement", clear_on_submit=True):
        title = st.text_input("Announcement Title", placeholder="e.g. Scheduled System Upgrades")
        content = st.text_area("Content Details", placeholder="Enter notice context...")
        
        submit_announce = st.form_submit_button("Publish Notice")
        
        if submit_announce:
            title = title.strip()
            content = content.strip()
            
            if not title or not content:
                st.error("All notice fields are required.")
            else:
                announcements = read_json(ANNOUNCEMENTS_FILE)
                if not isinstance(announcements, list):
                    announcements = []
                    
                new_id = max([a.get("id", 0) for a in announcements] + [0]) + 1
                new_notice = {
                    "id": new_id,
                    "title": title,
                    "content": content,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "author": st.session_state.fullname
                }
                
                announcements.insert(0, new_notice)
                if write_json(ANNOUNCEMENTS_FILE, announcements):
                    st.success(f"Published: '{title}'")
                    log_activity(st.session_state.username, "Post Notice", f"Published announcement: {title}")
                    st.rerun()
                else:
                    st.error("Failed to publish announcement.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("ℹ️ Announcement tools are locked. Only Admin role credentials can publish announcements.")

# 8. Render Footer
render_footer()
