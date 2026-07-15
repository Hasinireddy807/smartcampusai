import streamlit as st
import pandas as pd
from utils.helper import setup_page, log_activity, validate_email
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import FACULTY_FILE
from utils.json_db import read_json, write_json

# 1. Initialize Page Config & Styles
setup_page("Faculty Directory")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>Faculty Directory</h2>", unsafe_allow_html=True)

# Fetch roles to apply access control rules
user_role = st.session_state.get("role", "Student")
is_authorized_editor = user_role in ["Admin", "Faculty"]

faculty = read_json(FACULTY_FILE)
if not isinstance(faculty, list):
    faculty = []

# Directory search
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h4>Search Directory</h4>", unsafe_allow_html=True)
search_query = st.text_input("Filter faculty by Name, ID, or Specialization", "").strip().lower()

filtered_faculty = faculty
if search_query:
    filtered_faculty = [
        f for f in faculty if (
            search_query in f.get("name", "").lower() or
            search_query in f.get("id", "").lower() or
            search_query in f.get("specialization", "").lower() or
            search_query in f.get("department", "").lower()
        )
    ]

# Display Datatable
if filtered_faculty:
    df_faculty = pd.DataFrame(filtered_faculty)
    display_cols = ["id", "name", "email", "department", "designation", "specialization"]
    df_faculty = df_faculty[display_cols]
    st.dataframe(df_faculty, use_container_width=True, hide_index=True)
else:
    st.info("No matching faculty records found.")
st.markdown("</div>", unsafe_allow_html=True)

# CRUD section (Tabs)
if is_authorized_editor:
    st.markdown("<h3>Directory Operations</h3>", unsafe_allow_html=True)
    tab_add, tab_update, tab_delete = st.tabs(["➕ Add Faculty", "✏️ Update Faculty", "❌ Delete Faculty"])
    
    with tab_add:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        with st.form("form_add_faculty", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_id = st.text_input("Faculty ID (Unique)", placeholder="e.g. FAC004")
                new_name = st.text_input("Full Name", placeholder="e.g. Dr. Richard Feynman")
                new_email = st.text_input("Email Address", placeholder="e.g. feynman@smartcampus.edu")
            with col2:
                new_dept = st.selectbox("Department", ["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration"])
                new_desig = st.selectbox("Designation", ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"])
                new_spec = st.text_input("Specialization / Research Area", placeholder="e.g. Quantum Electrodynamics")
                
            submit_add = st.form_submit_button("Add Faculty Record")
            
            if submit_add:
                new_id = new_id.strip().upper()
                new_name = new_name.strip()
                new_email = new_email.strip()
                new_spec = new_spec.strip()
                
                # Validation checks
                if not new_id or not new_name or not new_email or not new_spec:
                    st.error("All fields are required.")
                elif not validate_email(new_email):
                    st.error("Invalid email address format.")
                elif any(f.get("id", "").upper() == new_id for f in faculty):
                    st.error(f"Faculty ID {new_id} already exists.")
                elif any(f.get("email", "").lower() == new_email.lower() for f in faculty):
                    st.error(f"Email {new_email} is already linked to another faculty member.")
                else:
                    new_record = {
                        "id": new_id,
                        "name": new_name,
                        "email": new_email,
                        "department": new_dept,
                        "designation": new_desig,
                        "specialization": new_spec
                    }
                    faculty.append(new_record)
                    if write_json(FACULTY_FILE, faculty):
                        st.success(f"Faculty {new_name} added to directory successfully!")
                        log_activity(st.session_state.username, "Add Faculty", f"Added faculty {new_name} ({new_id})")
                        st.rerun()
                    else:
                        st.error("Failed to update database.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_update:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        faculty_ids = [f.get("id") for f in faculty]
        if faculty_ids:
            target_id = st.selectbox("Select Faculty ID to Update", faculty_ids)
            selected_fac = next(f for f in faculty if f.get("id") == target_id)
            
            with st.form("form_update_faculty"):
                col1, col2 = st.columns(2)
                with col1:
                    up_name = st.text_input("Full Name", value=selected_fac.get("name"))
                    up_email = st.text_input("Email Address", value=selected_fac.get("email"))
                with col2:
                    up_dept = st.selectbox("Department", 
                                           ["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration"],
                                           index=["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration"].index(selected_fac.get("department", "Computer Science")))
                    up_desig = st.selectbox("Designation", 
                                            ["Professor", "Associate Professor", "Assistant Professor", "Lecturer"],
                                            index=["Professor", "Associate Professor", "Assistant Professor", "Lecturer"].index(selected_fac.get("designation", "Professor")))
                    up_spec = st.text_input("Specialization / Research Area", value=selected_fac.get("specialization"))
                
                submit_update = st.form_submit_button("Update Faculty Record")
                
                if submit_update:
                    up_name = up_name.strip()
                    up_email = up_email.strip()
                    up_spec = up_spec.strip()
                    
                    if not up_name or not up_email or not up_spec:
                        st.error("Fields cannot be empty.")
                    elif not validate_email(up_email):
                        st.error("Invalid email address format.")
                    else:
                        # Check duplicate email on other records
                        email_dup = False
                        for f in faculty:
                            if f.get("id") != target_id and f.get("email", "").lower() == up_email.lower():
                                email_dup = True
                                break
                        
                        if email_dup:
                            st.error(f"Email {up_email} is registered with another faculty member.")
                        else:
                            for idx, f in enumerate(faculty):
                                if f.get("id") == target_id:
                                    faculty[idx]["name"] = up_name
                                    faculty[idx]["email"] = up_email
                                    faculty[idx]["department"] = up_dept
                                    faculty[idx]["designation"] = up_desig
                                    faculty[idx]["specialization"] = up_spec
                                    break
                            
                            if write_json(FACULTY_FILE, faculty):
                                st.success(f"Faculty member {target_id} updated successfully!")
                                log_activity(st.session_state.username, "Update Faculty", f"Updated faculty ID: {target_id}")
                                st.rerun()
                            else:
                                st.error("Failed to update database.")
        else:
            st.info("No faculty records available to update.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_delete:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        faculty_ids_del = [f.get("id") for f in faculty]
        if faculty_ids_del:
            target_del_id = st.selectbox("Select Faculty ID to Delete", faculty_ids_del, key="sb_fac_del_id")
            selected_del_fac = next(f for f in faculty if f.get("id") == target_del_id)
            
            st.warning(f"⚠️ Are you sure you want to permanently delete **{selected_del_fac.get('name')} ({target_del_id})**?")
            confirm_delete = st.button("🔴 Confirm Delete Faculty Member")
            
            if confirm_delete:
                faculty = [f for f in faculty if f.get("id") != target_del_id]
                if write_json(FACULTY_FILE, faculty):
                    st.success(f"Faculty member {target_del_id} removed from directory.")
                    log_activity(st.session_state.username, "Delete Faculty", f"Deleted faculty ID: {target_del_id}")
                    st.rerun()
                else:
                    st.error("Failed to delete record.")
        else:
            st.info("No faculty records available to delete.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("ℹ️ Faculty directories are in read-only mode for your role. Contact an administrator to add or modify faculty members.")

# 8. Render Footer
render_footer()
