import streamlit as st
import pandas as pd
import datetime
from utils.helper import setup_page, log_activity
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import ATTENDANCE_FILE, STUDENTS_FILE
from utils.json_db import read_json, write_json

# 1. Initialize Page Config & Styles
setup_page("Attendance Tracker")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>Attendance Tracker</h2>", unsafe_allow_html=True)

# Role configurations
user_role = st.session_state.get("role", "Student")
is_authorized_editor = user_role in ["Admin", "Faculty"]

attendance = read_json(ATTENDANCE_FILE)
if not isinstance(attendance, list):
    attendance = []

students = read_json(STUDENTS_FILE)
if not isinstance(students, list):
    students = []

# Section 1: Record Attendance Form (restricted)
if is_authorized_editor:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h3>📝 Log Student Attendance</h3>", unsafe_allow_html=True)
    
    student_opts = {s.get("id"): f"{s.get('name')} ({s.get('id')})" for s in students}
    
    if student_opts:
        with st.form("form_log_attendance", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                selected_student_id = st.selectbox("Select Student", list(student_opts.keys()), format_func=lambda x: student_opts[x])
                subject = st.text_input("Course Code / Subject", placeholder="e.g. CS-101").strip().upper()
            with col2:
                status = st.selectbox("Attendance Status", ["Present", "Absent"])
                att_date = st.date_input("Date", datetime.date.today())
                
            submit_att = st.form_submit_button("Record Attendance")
            
            if submit_att:
                if not subject:
                    st.error("Course / Subject code is required.")
                else:
                    new_log = {
                        "date": str(att_date),
                        "student_id": selected_student_id,
                        "status": status,
                        "subject": subject
                    }
                    
                    # Prevent duplicate log for same date, student, and subject
                    duplicate = any(
                        log.get("date") == str(att_date) and
                        log.get("student_id") == selected_student_id and
                        log.get("subject") == subject
                        for log in attendance
                    )
                    
                    if duplicate:
                        st.error(f"Attendance for student {selected_student_id} in course {subject} is already logged on {att_date}.")
                    else:
                        attendance.insert(0, new_log)
                        if write_json(ATTENDANCE_FILE, attendance):
                            st.success(f"Successfully recorded '{status}' for student {selected_student_id} in {subject}.")
                            log_activity(st.session_state.username, "Log Attendance", f"Logged {status} for student ID {selected_student_id} in {subject}")
                            st.rerun()
                        else:
                            st.error("Failed to write to database.")
    else:
        st.info("No registered students found in the database. Please register students first.")
    st.markdown("</div>", unsafe_allow_html=True)

# Section 2: View and Filter logs
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h3>📋 Attendance Registry</h3>", unsafe_allow_html=True)

if attendance:
    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns(3)
    
    # Get unique search suggestions
    subjects_list = sorted(list(set(log.get("subject", "") for log in attendance)))
    student_ids_list = sorted(list(set(log.get("student_id", "") for log in attendance)))
    
    with col_f1:
        f_subject = st.selectbox("Filter Course", ["All"] + subjects_list)
    with col_f2:
        f_student = st.selectbox("Filter Student ID", ["All"] + student_ids_list)
    with col_f3:
        f_status = st.selectbox("Filter Status", ["All", "Present", "Absent"])
        
    # Filter database
    filtered_logs = attendance
    if f_subject != "All":
        filtered_logs = [log for log in filtered_logs if log.get("subject") == f_subject]
    if f_student != "All":
        filtered_logs = [log for log in filtered_logs if log.get("student_id") == f_student]
    if f_status != "All":
        filtered_logs = [log for log in filtered_logs if log.get("status") == f_status]
        
    # Render table
    if filtered_logs:
        df_logs = pd.DataFrame(filtered_logs)
        
        # Merge with student names for clarity
        if students:
            df_stud = pd.DataFrame(students)
            df_merged = pd.merge(df_logs, df_stud[["id", "name"]], left_on="student_id", right_on="id", how="left")
            # Clean merged columns
            if "name" in df_merged.columns:
                df_merged["Student Name"] = df_merged["name"]
                df_merged = df_merged.drop(columns=["id", "name"], errors="ignore")
                
            display_cols = ["date", "student_id", "Student Name", "subject", "status"]
            df_merged = df_merged[display_cols]
            st.dataframe(df_merged, use_container_width=True, hide_index=True)
        else:
            st.dataframe(df_logs[["date", "student_id", "subject", "status"]], use_container_width=True, hide_index=True)
            
        # Display aggregate stats
        p_count = sum(log.get("status") == "Present" for log in filtered_logs)
        total_count = len(filtered_logs)
        rate = (p_count / total_count * 100) if total_count > 0 else 0
        st.markdown(f"**Filtered Summary**: {p_count} Present / {total_count} Total &mdash; Attendance Rate: **{rate:.1f}%**")
    else:
        st.info("No attendance records match the selected filters.")
else:
    st.info("No attendance logs recorded in the database.")
    
st.markdown("</div>", unsafe_allow_html=True)

# 8. Render Footer
render_footer()
