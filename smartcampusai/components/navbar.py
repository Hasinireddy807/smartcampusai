import streamlit as st
import datetime

def render_navbar():
    """
    Renders a premium top navigation bar with date, user greetings, and status indicator.
    """
    now = datetime.datetime.now().strftime("%A, %b %d, %Y")
    username = st.session_state.get("username", "Guest")
    fullname = st.session_state.get("fullname", "Guest User")
    role = st.session_state.get("role", "Student")
    
    # Custom colored badge based on user role
    role_colors = {
        "Admin": "linear-gradient(135deg, #ef4444, #f97316)",
        "Faculty": "linear-gradient(135deg, #3b82f6, #06b6d4)",
        "Student": "linear-gradient(135deg, #10b981, #84cc16)"
    }
    bg_gradient = role_colors.get(role, "linear-gradient(135deg, #6b7280, #9ca3af)")
    
    st.markdown(
        f"""
        <div style="
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            background: rgba(15, 23, 42, 0.6); 
            border: 1px solid rgba(255,255,255,0.08); 
            padding: 0.8rem 1.5rem; 
            border-radius: 12px; 
            margin-bottom: 2rem;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        ">
            <div style="display: flex; align-items: center; gap: 10px;">
                <span class="pulse-indicator"></span>
                <span style="font-size: 0.9rem; color: #94a3b8; font-weight: 500;">SYSTEM LIVE</span>
                <span style="color: rgba(255,255,255,0.15)">|</span>
                <span style="font-size: 0.9rem; color: #f8fafc; font-weight: 500;">{now}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="text-align: right;">
                    <div style="font-size: 0.95rem; color: #f8fafc; font-weight: 600;">{fullname}</div>
                    <div style="font-size: 0.75rem; color: #94a3b8; font-weight: 400;">@{username}</div>
                </div>
                <div style="
                    background: {bg_gradient}; 
                    color: white; 
                    padding: 0.25rem 0.75rem; 
                    border-radius: 20px; 
                    font-size: 0.75rem; 
                    font-weight: 700;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">
                    {role}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
