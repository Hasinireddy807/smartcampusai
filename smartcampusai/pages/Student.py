import streamlit as st
import pandas as pd
from utils.helper import setup_page, log_activity, validate_email
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import STUDENTS_FILE
from utils.json_db import read_json, write_json

# 1. Initialize Page Config & Styles
setup_page("Student Management")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>Student Management Directory</h2>", unsafe_allow_html=True)

# Fetch roles to apply access control rules (Admins and Faculty can edit, Students can only view)
user_role = st.session_state.get("role", "Student")
is_authorized_editor = user_role in ["Admin", "Faculty"]

students = read_json(STUDENTS_FILE)
if not isinstance(students, list):
    students = []

# Directory search
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h4>Search Directory</h4>", unsafe_allow_html=True)
search_query = st.text_input("Filter students by Name, ID, or Department", "").strip().lower()

filtered_students = students
if search_query:
    filtered_students = [
        s for s in students if (
            search_query in s.get("name", "").lower() or
            search_query in s.get("id", "").lower() or
            search_query in s.get("department", "").lower()
        )
    ]

# Display Datatable
if filtered_students:
    df_students = pd.DataFrame(filtered_students)
    # Reorder columns for display
    display_cols = ["id", "name", "email", "department", "enrollment_year", "status"]
    df_students = df_students[display_cols]
    st.dataframe(df_students, use_container_width=True, hide_index=True)
else:
    st.info("No matching students found in the database.")
st.markdown("</div>", unsafe_allow_html=True)

# CRUD section (Tabs)
if is_authorized_editor:
    st.markdown("<h3>Directory Operations</h3>", unsafe_allow_html=True)
    tab_add, tab_update, tab_delete = st.tabs(["➕ Add Student", "✏️ Update Student", "❌ Delete Student"])
    
    with tab_add:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        with st.form("form_add_student", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                new_id = st.text_input("Student ID (Unique)", placeholder="e.g. STU006")
                new_name = st.text_input("Full Name", placeholder="e.g. Liam Neeson")
                new_email = st.text_input("Email Address", placeholder="e.g. liam@smartcampus.edu")
            with col2:
                new_dept = st.selectbox("Department", ["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration"])
                new_year = st.number_input("Enrollment Year", min_value=2015, max_value=2030, value=2026)
                new_status = st.selectbox("Enrollment Status", ["Active", "Suspended", "Alumni"])
                
            submit_add = st.form_submit_button("Add Student Record")
            
            if submit_add:
                new_id = new_id.strip().upper()
                new_name = new_name.strip()
                new_email = new_email.strip()
                
                # Validation checks
                if not new_id or not new_name or not new_email:
                    st.error("All fields are required.")
                elif not validate_email(new_email):
                    st.error("Invalid email address format.")
                elif any(s.get("id", "").upper() == new_id for s in students):
                    st.error(f"Student ID {new_id} already exists.")
                elif any(s.get("email", "").lower() == new_email.lower() for s in students):
                    st.error(f"Email {new_email} is already linked to another student.")
                else:
                    new_record = {
                        "id": new_id,
                        "name": new_name,
                        "email": new_email,
                        "department": new_dept,
                        "enrollment_year": int(new_year),
                        "status": new_status
                    }
                    students.append(new_record)
                    if write_json(STUDENTS_FILE, students):
                        st.success(f"Student {new_name} registered successfully!")
                        log_activity(st.session_state.username, "Add Student", f"Added {new_name} ({new_id})")
                        st.rerun()
                    else:
                        st.error("Failed to update database.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_update:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        # Select student to update
        student_ids = [s.get("id") for s in students]
        if student_ids:
            target_id = st.selectbox("Select Student ID to Update", student_ids)
            selected_student = next(s for s in students if s.get("id") == target_id)
            
            with st.form("form_update_student"):
                col1, col2 = st.columns(2)
                with col1:
                    up_name = st.text_input("Full Name", value=selected_student.get("name"))
                    up_email = st.text_input("Email Address", value=selected_student.get("email"))
                with col2:
                    up_dept = st.selectbox("Department", 
                                           ["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration"],
                                           index=["Computer Science", "Data Science", "Electrical Engineering", "Mechanical Engineering", "Business Administration"].index(selected_student.get("department", "Computer Science")))
                    up_year = st.number_input("Enrollment Year", min_value=2015, max_value=2030, value=selected_student.get("enrollment_year", 2024))
                    up_status = st.selectbox("Enrollment Status", ["Active", "Suspended", "Alumni"], index=["Active", "Suspended", "Alumni"].index(selected_student.get("status", "Active")))
                
                submit_update = st.form_submit_button("Update Student Record")
                
                if submit_update:
                    up_name = up_name.strip()
                    up_email = up_email.strip()
                    
                    if not up_name or not up_email:
                        st.error("Fields cannot be empty.")
                    elif not validate_email(up_email):
                        st.error("Invalid email address format.")
                    else:
                        # Check duplicate email on other records
                        email_dup = False
                        for s in students:
                            if s.get("id") != target_id and s.get("email", "").lower() == up_email.lower():
                                email_dup = True
                                break
                        
                        if email_dup:
                            st.error(f"Email {up_email} is registered with another student.")
                        else:
                            for idx, s in enumerate(students):
                                if s.get("id") == target_id:
                                    students[idx]["name"] = up_name
                                    students[idx]["email"] = up_email
                                    students[idx]["department"] = up_dept
                                    students[idx]["enrollment_year"] = int(up_year)
                                    students[idx]["status"] = up_status
                                    break
                            
                            if write_json(STUDENTS_FILE, students):
                                st.success(f"Student {target_id} updated successfully!")
                                log_activity(st.session_state.username, "Update Student", f"Updated student ID: {target_id}")
                                st.rerun()
                            else:
                                st.error("Failed to update database.")
        else:
            st.info("No student records available to update.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with tab_delete:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        student_ids_del = [s.get("id") for s in students]
        if student_ids_del:
            target_del_id = st.selectbox("Select Student ID to Delete", student_ids_del, key="sb_del_id")
            selected_del_student = next(s for s in students if s.get("id") == target_del_id)
            
            st.warning(f"⚠️ Are you sure you want to permanently delete **{selected_del_student.get('name')} ({target_del_id})**?")
            confirm_delete = st.button("🔴 Confirm Delete Student")
            
            if confirm_delete:
                students = [s for s in students if s.get("id") != target_del_id]
                if write_json(STUDENTS_FILE, students):
                    st.success(f"Student {target_del_id} removed from registry.")
                    log_activity(st.session_state.username, "Delete Student", f"Deleted student ID: {target_del_id}")
                    st.rerun()
                else:
                    st.error("Failed to delete record.")
        else:
            st.info("No student records available to delete.")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("ℹ️ Student directories are in read-only mode for your role. Contact an administrator to add or modify student data.")

# 8. Render Footer
render_footer()
