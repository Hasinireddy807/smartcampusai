import streamlit as st
import pandas as pd
from utils.helper import setup_page, log_activity
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.cards import render_kpi_card
from components.footer import render_footer
from utils.config import STUDENTS_FILE, FACULTY_FILE, ATTENDANCE_FILE, ACTIVITY_FILE, ANNOUNCEMENTS_FILE
from utils.json_db import read_json
from utils.charts import (
    create_attendance_trend_chart, 
    create_department_distribution_chart, 
    create_student_growth_chart
)

# 1. Initialize Page Config & Styles
setup_page("Dashboard")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

# 4. Read Data Sources
students = read_json(STUDENTS_FILE)
faculty = read_json(FACULTY_FILE)
attendance = read_json(ATTENDANCE_FILE)
activities = read_json(ACTIVITY_FILE)
announcements = read_json(ANNOUNCEMENTS_FILE)

# Calculate Stats
total_students = len(students)
total_faculty = len(faculty)

# Calculate average attendance rate
if attendance:
    df_att = pd.DataFrame(attendance)
    if "status" in df_att.columns:
        present_count = sum(df_att["status"] == "Present")
        total_att = len(df_att)
        avg_attendance = f"{(present_count / total_att * 100):.1f}%"
    else:
        avg_attendance = "0.0%"
else:
    avg_attendance = "0.0%"

# Calculate AI assistant query requests from logs
ai_requests = sum(1 for act in activities if act.get("action") == "AI Query")

# 5. Top KPI Cards row
st.markdown("<h3 style='margin-bottom: 1rem; color:#f8fafc;'>Campus Overview</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    render_kpi_card("Total Students", total_students, "Registered active students", "👨‍🎓", "#6366f1")
with col2:
    render_kpi_card("Active Faculty", total_faculty, "Faculty members directory", "👩‍🏫", "#a855f7")
with col3:
    render_kpi_card("Avg. Attendance", avg_attendance, "Overall attendance rate", "📅", "#10b981")
with col4:
    render_kpi_card("AI Requests", ai_requests, "Total assistant calls", "⚡", "#ec4899")

st.markdown("<br>", unsafe_allow_html=True)

# 6. Charts Layout
st.markdown("<h3 style='color:#f8fafc;'>Analytics Insights</h3>", unsafe_allow_html=True)
c_col1, c_col2 = st.columns(2)

with c_col1:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    fig_attendance = create_attendance_trend_chart(attendance)
    st.plotly_chart(fig_attendance, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c_col2:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    fig_dept = create_department_distribution_chart(students)
    st.plotly_chart(fig_dept, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Student growth over years chart
st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
fig_growth = create_student_growth_chart(students)
st.plotly_chart(fig_growth, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# 7. Quick Actions, Announcements, and Recent Activity Grid
col_left, col_right = st.columns([1, 1])

with col_left:
    st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top: 0; color:#f8fafc;'>Quick Actions</h4>", unsafe_allow_html=True)
    
    # We can provide simple redirects using columns/buttons
    act_col1, act_col2 = st.columns(2)
    with act_col1:
        if st.button("➕ Register Student", key="btn_quick_reg_stu"):
            st.switch_page("pages/Student.py")
        if st.button("🤖 Launch Assistant", key="btn_quick_ai"):
            st.switch_page("pages/AI_Assistant.py")
    with act_col2:
        if st.button("📝 Log Attendance", key="btn_quick_att"):
            st.switch_page("pages/Attendance.py")
        if st.button("⚙️ Manage Settings", key="btn_quick_sett"):
            st.switch_page("pages/Settings.py")
            
    st.markdown("<h4 style='margin-top: 1.5rem; color:#f8fafc;'>Recent Announcements</h4>", unsafe_allow_html=True)
    if announcements:
        for item in announcements[:3]:
            st.markdown(
                f"""
                <div style="
                    border-left: 3px solid #a855f7; 
                    padding-left: 10px; 
                    margin-bottom: 1rem;
                    background: rgba(255,255,255,0.02);
                    padding: 8px 12px;
                    border-radius: 0 8px 8px 0;
                ">
                    <strong style="color: #f8fafc; font-size:0.9rem;">{item.get('title')}</strong><br>
                    <span style="color: #94a3b8; font-size: 0.8rem;">{item.get('date')} &bull; By {item.get('author')}</span>
                    <p style="margin: 4px 0 0; color: #cbd5e1; font-size: 0.85rem;">{item.get('content')}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No active announcements.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='glass-card' style='height: 100%;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top: 0; color:#f8fafc;'>Recent System Activity</h4>", unsafe_allow_html=True)
    
    if activities:
        df_act = pd.DataFrame(activities[:6])
        # Display as a styled table
        st.dataframe(
            df_act[["timestamp", "username", "action", "details"]], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.write("No system activity logs found.")
        
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Render Footer
render_footer()
