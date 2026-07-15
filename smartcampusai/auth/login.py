import streamlit as st
from auth.authentication import authenticate_user

def render_login_form():
    """Renders the login UI form."""
    st.markdown("<div class='glass-card animate-fade-in'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gradient-text' style='margin-top:0;'>SmartCampusAI Login</h2>", unsafe_allow_html=True)
    st.write("Welcome back! Please enter your credentials to manage and view campus insights.")
    
    # Form input fields
    username_or_email = st.text_input("Username or Email Address", placeholder="e.g. jsmith or jsmith@domain.edu")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    submit = st.button("Log In")
    
    if submit:
        if not username_or_email or not password:
            st.error("Please fill in both the username/email and password fields.")
        else:
            with st.spinner("Authenticating..."):
                success, msg = authenticate_user(username_or_email, password)
                if success:
                    st.toast("🔑 Login Successful! Redirecting...", icon="🎉")
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
                    
    st.markdown("</div>", unsafe_allow_html=True)
