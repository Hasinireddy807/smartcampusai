import os
import streamlit as st
from PIL import Image
from utils.session import logout_user
from utils.config import ASSETS_DIR

def render_sidebar():
    """
    Injects custom items (logo, avatar card, logout button) into the Streamlit sidebar.
    """
    st.sidebar.markdown("<div style='margin-bottom: 1rem;'>", unsafe_allow_html=True)
    
    # 1. Try to load and render the logo
    logo_path = os.path.join(ASSETS_DIR, "logo.png")
    if os.path.exists(logo_path):
        try:
            logo_img = Image.open(logo_path)
            st.sidebar.image(logo_img, use_column_width=True)
        except Exception:
            st.sidebar.title("SmartCampusAI")
    else:
        st.sidebar.title("SmartCampusAI")
        
    st.sidebar.markdown("</div>", unsafe_allow_html=True)
    
    # 2. Render Avatar & User Greeting Card
    st.sidebar.markdown(
        """
        <div style="
            background: rgba(30, 41, 59, 0.4); 
            border: 1px solid rgba(255, 255, 255, 0.05); 
            border-radius: 12px; 
            padding: 1rem; 
            margin-bottom: 2rem;
            text-align: center;
        ">
        """, 
        unsafe_allow_html=True
    )
    
    avatar_path = os.path.join(ASSETS_DIR, "avatar.png")
    if os.path.exists(avatar_path):
        try:
            avatar_img = Image.open(avatar_path)
            st.sidebar.image(avatar_img, width=80)
        except Exception:
            pass
            
    fullname = st.session_state.get("fullname", "User Profile")
    role = st.session_state.get("role", "Student")
    
    st.sidebar.markdown(
        f"""
            <h4 style="margin: 0.5rem 0 0.2rem; color: #f8fafc;">{fullname}</h4>
            <p style="margin: 0; font-size: 0.8rem; color: #a855f7; font-weight: 600; text-transform: uppercase;">{role}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Sidebar quick instructions
    st.sidebar.markdown(
        """
        <div style="font-size: 0.75rem; color: #64748b; padding: 0.5rem; margin-bottom: 1rem;">
            <strong>Quick Note:</strong> Navigate using the page links above. Changes to students, faculty, or attendance are persisted automatically.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 3. Render Logout button
    st.sidebar.markdown("---")
    if st.sidebar.button("🔒 Log Out", key="sidebar_logout_btn"):
        logout_user()
        st.toast("🔒 Logged out successfully.", icon="👋")
        st.switch_page("app.py")
        st.stop()
