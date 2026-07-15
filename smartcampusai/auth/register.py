import streamlit as st
from auth.authentication import register_user

def render_register_form():
    """Renders the user registration form interface."""
    st.markdown("<div class='glass-card animate-fade-in'>", unsafe_allow_html=True)
    st.markdown("<h2 class='gradient-text' style='margin-top:0;'>Create Account</h2>", unsafe_allow_html=True)
    st.write("Join the SmartCampusAI platform. Get analytical insights and virtual assistance.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fullname = st.text_input("Full Name", placeholder="e.g. John Smith")
        username = st.text_input("Username", placeholder="e.g. jsmith")
        email = st.text_input("Email Address", placeholder="e.g. jsmith@domain.edu")
        
    with col2:
        role = st.selectbox("Your Role", ["Student", "Faculty", "Admin"])
        password = st.text_input("Password", type="password", placeholder="Minimum 8 chars, 1 uppercase, 1 digit, 1 symbol")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
        
    submit = st.button("Register")
    
    if submit:
        success, msg = register_user(
            fullname=fullname,
            username=username,
            email=email,
            password=password,
            confirm_password=confirm_password,
            role=role
        )
        if success:
            st.success(msg)
            st.balloons()
        else:
            st.error(msg)
            
    st.markdown("</div>", unsafe_allow_html=True)
