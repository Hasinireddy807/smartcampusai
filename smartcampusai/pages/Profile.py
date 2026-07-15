import streamlit as st
from utils.helper import setup_page, log_activity, validate_password_strength
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import USERS_FILE
from utils.json_db import read_json, write_json
from auth.password_utils import hash_password, check_password

# 1. Initialize Page Config & Styles
setup_page("User Profile")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>My Profile</h2>", unsafe_allow_html=True)

# Fetch user details
username = st.session_state.get("username")
users = read_json(USERS_FILE)
current_user = next((u for u in users if u.get("username") == username), None)

if current_user:
    col_details, col_edit = st.columns([1, 1])
    
    with col_details:
        st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
        st.markdown("<h4>Profile Details</h4>", unsafe_allow_html=True)
        
        st.markdown(
            f"""
            <div style="line-height: 2;">
                <strong>Full Name:</strong> {current_user.get('fullname')}<br>
                <strong>Username:</strong> @{current_user.get('username')}<br>
                <strong>Email Address:</strong> {current_user.get('email')}<br>
                <strong>System Role:</strong> <span style="color: #a855f7; font-weight:700;">{current_user.get('role')}</span><br>
                <strong>Joined Since:</strong> {current_user.get('registration_date')}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_edit:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Update Details</h4>", unsafe_allow_html=True)
        
        with st.form("form_edit_profile"):
            new_fullname = st.text_input("Full Name", value=current_user.get("fullname"))
            submit_name = st.form_submit_button("Save Profile Info")
            
            if submit_name:
                new_fullname = new_fullname.strip()
                if not new_fullname:
                    st.error("Name cannot be empty.")
                else:
                    # Update users database record
                    for idx, u in enumerate(users):
                        if u.get("username") == username:
                            users[idx]["fullname"] = new_fullname
                            break
                            
                    if write_json(USERS_FILE, users):
                        st.session_state.fullname = new_fullname
                        st.success("Profile details updated successfully!")
                        log_activity(username, "Update Profile", "Updated full name info")
                        st.rerun()
                    else:
                        st.error("Failed to update database.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Change password module
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Change Password</h4>", unsafe_allow_html=True)
    
    with st.form("form_change_password"):
        curr_pass = st.text_input("Current Password", type="password")
        new_pass = st.text_input("New Password", type="password", placeholder="Minimum 8 chars, 1 upper, 1 digit, 1 symbol")
        confirm_pass = st.text_input("Confirm New Password", type="password")
        
        submit_pass = st.form_submit_button("Update Password")
        
        if submit_pass:
            curr_pass = curr_pass.strip()
            new_pass = new_pass.strip()
            confirm_pass = confirm_pass.strip()
            
            # 1. Verify inputs
            if not curr_pass or not new_pass or not confirm_pass:
                st.error("All password fields are required.")
            # 2. Check current password matches
            elif not check_password(curr_pass, current_user.get("password", "")):
                st.error("Current password entered is incorrect.")
            # 3. Check new password match
            elif new_pass != confirm_pass:
                st.error("New passwords do not match.")
            # 4. Strength check
            else:
                is_strong, msg = validate_password_strength(new_pass)
                if not is_strong:
                    st.error(msg)
                else:
                    # Update hashed password
                    hashed_new = hash_password(new_pass)
                    for idx, u in enumerate(users):
                        if u.get("username") == username:
                            users[idx]["password"] = hashed_new
                            break
                            
                    if write_json(USERS_FILE, users):
                        st.success("Password changed successfully!")
                        log_activity(username, "Change Password", "Changed account password credentials")
                        st.rerun()
                    else:
                        st.error("Failed to update password.")
                        
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.error("Critical: User record could not be loaded.")

# 8. Render Footer
render_footer()
