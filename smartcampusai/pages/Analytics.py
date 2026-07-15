import streamlit as st
import pandas as pd
import plotly.express as px
from utils.helper import setup_page
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import STUDENTS_FILE, FACULTY_FILE, ATTENDANCE_FILE
from utils.json_db import read_json

# 1. Initialize Page Config & Styles
setup_page("Analytics")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>Advanced Analytics & Metrics</h2>", unsafe_allow_html=True)
st.write("Gain deep operations insights, audit student rosters, and view faculty ratios across campus departments.")

# Load data
students = read_json(STUDENTS_FILE)
faculty = read_json(FACULTY_FILE)
attendance = read_json(ATTENDANCE_FILE)

# Convert to dataframes
df_stu = pd.DataFrame(students) if students else pd.DataFrame(columns=["id", "name", "email", "department", "enrollment_year", "status"])
df_fac = pd.DataFrame(faculty) if faculty else pd.DataFrame(columns=["id", "name", "email", "department", "designation", "specialization"])
df_att = pd.DataFrame(attendance) if attendance else pd.DataFrame(columns=["date", "student_id", "status", "subject"])

tab_dept, tab_att, tab_ratios = st.tabs(["🏛️ Department Analysis", "📅 Attendance Insights", "📊 Ratios & Loads"])

with tab_dept:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Department Enrollment Distribution</h4>", unsafe_allow_html=True)
    
    if not df_stu.empty:
        # Pie Chart of departments
        dept_counts = df_stu["department"].value_counts().reset_index()
        dept_counts.columns = ["Department", "Number of Students"]
        
        fig_dept = px.pie(
            dept_counts, 
            names="Department", 
            values="Number of Students", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        fig_dept.update_layout(
            template="plotly_dark", 
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_dept, use_container_width=True)
        
        # Details Table
        st.markdown("<h5>Department Summary Table</h5>", unsafe_allow_html=True)
        dept_summary = df_stu.groupby("department").agg(
            Total_Students=("id", "count"),
            Active_Students=("status", lambda x: sum(x == "Active")),
            Avg_Enrollment_Year=("enrollment_year", "mean")
        ).round(1).reset_index()
        st.dataframe(dept_summary, use_container_width=True, hide_index=True)
    else:
        st.info("No student records available for department analysis.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_att:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Course Attendance Distribution</h4>", unsafe_allow_html=True)
    
    if not df_att.empty:
        # Group by Course/Subject and Status
        course_att = df_att.groupby(["subject", "status"]).size().unstack(fill_value=0)
        
        if "Present" not in course_att.columns:
            course_att["Present"] = 0
        if "Absent" not in course_att.columns:
            course_att["Absent"] = 0
            
        course_att["Total"] = course_att["Present"] + course_att["Absent"]
        course_att["Attendance Rate (%)"] = (course_att["Present"] / course_att["Total"] * 100).round(1)
        course_att = course_att.reset_index()
        
        # Bar Chart of course rates
        fig_course = px.bar(
            course_att, 
            x="subject", 
            y="Attendance Rate (%)",
            color="Attendance Rate (%)",
            title="Attendance rate by Course/Subject",
            color_continuous_scale="Sunsetdark"
        )
        fig_course.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.4)",
            xaxis_title="Course Code",
            yaxis_title="Rate (%)",
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_course, use_container_width=True)
        
        # Logs details
        st.dataframe(course_att[["subject", "Present", "Absent", "Total", "Attendance Rate (%)"]], use_container_width=True, hide_index=True)
    else:
        st.info("No attendance records logged to produce insights.")
    st.markdown("</div>", unsafe_allow_html=True)

with tab_ratios:
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h4>Faculty load and Student-to-Teacher Ratios</h4>", unsafe_allow_html=True)
    
    if not df_stu.empty and not df_fac.empty:
        stu_depts = df_stu["department"].value_counts().reset_index()
        stu_depts.columns = ["Department", "Student Count"]
        
        fac_depts = df_fac["department"].value_counts().reset_index()
        fac_depts.columns = ["Department", "Faculty Count"]
        
        ratio_df = pd.merge(stu_depts, fac_depts, on="Department", how="outer").fillna(0)
        
        # Calculate ratio
        ratio_df["Students per Faculty"] = (ratio_df["Student Count"] / ratio_df["Faculty Count"]).round(1)
        # Handle division by zero
        ratio_df.loc[ratio_df["Faculty Count"] == 0, "Students per Faculty"] = ratio_df["Student Count"]
        
        # Render a grouped bar chart
        fig_ratio = px.bar(
            ratio_df,
            x="Department",
            y=["Student Count", "Faculty Count"],
            barmode="group",
            title="Student and Faculty count per Department",
            color_discrete_map={"Student Count": "#6366f1", "Faculty Count": "#ec4899"}
        )
        fig_ratio.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.4)"
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
        
        st.dataframe(ratio_df, use_container_width=True, hide_index=True)
    else:
        st.info("Ratios cannot be calculated without both Student and Faculty database records.")
    st.markdown("</div>", unsafe_allow_html=True)

# 8. Render Footer
render_footer()
