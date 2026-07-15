import os
import streamlit as st
from utils.helper import setup_page
from utils.config import ASSETS_DIR
from PIL import Image
from auth.authentication import check_auth
from auth.login import render_login_form
from auth.register import render_register_form
from components.footer import render_footer

# 1. Initialize page configuration, session variables, and custom CSS
setup_page("Gateway")

# 2. Redirect to Dashboard if already authenticated
if check_auth():
    st.switch_page("pages/Dashboard.py")
    st.stop()

# 3. Render modern header banner & layout
banner_path = os.path.join(ASSETS_DIR, "banner.png")
if os.path.exists(banner_path):
    try:
        banner_img = Image.open(banner_path)
        st.image(banner_img, use_column_width=True)
    except Exception:
        # Fallback text banner if Pillow loading fails
        st.markdown(
            """
            <div style="
                background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); 
                padding: 3rem; 
                border-radius: 16px; 
                text-align: center; 
                margin-bottom: 2rem;
                border: 1px solid rgba(255,255,255,0.08);
            ">
                <h1 style="color: #ffffff; font-weight:800; margin: 0; font-size: 2.5rem;">SmartCampusAI</h1>
                <p style="color: #cbd5e1; font-size: 1.1rem; margin-top: 0.5rem;">AI-Driven Education & Operations Command</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
else:
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #1e1b4b 0%, #311042 100%); 
            padding: 3rem; 
            border-radius: 16px; 
            text-align: center; 
            margin-bottom: 2rem;
            border: 1px solid rgba(255,255,255,0.08);
        ">
            <h1 style="color: #ffffff; font-weight:800; margin: 0; font-size: 2.5rem;">SmartCampusAI</h1>
            <p style="color: #cbd5e1; font-size: 1.1rem; margin-top: 0.5rem;">AI-Driven Education & Operations Command</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

# 4. Render main authentication container
st.markdown("<div style='max-width: 800px; margin: 0 auto;'>", unsafe_allow_html=True)

# Tabs to select between Login and Registration
auth_tab = st.radio(
    "Choose Action", 
    ["Sign In", "Create Account"], 
    horizontal=True,
    label_visibility="collapsed"
)

if auth_tab == "Sign In":
    render_login_form()
else:
    render_register_form()

st.markdown("</div>", unsafe_allow_html=True)

# 5. Render Footer
render_footer()
