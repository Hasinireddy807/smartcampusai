import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_attendance_trend_chart(attendance_data):
    """
    Generates a Plotly Line chart depicting daily attendance rates.
    """
    if not attendance_data:
        # Fallback empty chart layout
        fig = go.Figure()
        fig.update_layout(
            title="No Attendance Data Available",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

    df = pd.DataFrame(attendance_data)
    
    # Calculate attendance percentage per day
    df_grouped = df.groupby(["date", "status"]).size().unstack(fill_value=0)
    
    # Check if "Present" is in status columns
    if "Present" not in df_grouped.columns:
        df_grouped["Present"] = 0
    if "Absent" not in df_grouped.columns:
        df_grouped["Absent"] = 0
        
    df_grouped["Total"] = df_grouped["Present"] + df_grouped["Absent"]
    df_grouped["Attendance Rate (%)"] = (df_grouped["Present"] / df_grouped["Total"] * 100).round(2)
    df_grouped = df_grouped.reset_index()

    fig = px.line(
        df_grouped, 
        x="date", 
        y="Attendance Rate (%)",
        markers=True,
        title="Daily Student Attendance Rate (%)",
        color_discrete_sequence=["#a855f7"]
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        xaxis=dict(showgrid=False, title="Date"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Rate (%)", range=[0, 105]),
        margin=dict(l=40, r=40, t=50, b=40),
        hovermode="x unified"
    )
    fig.update_traces(line=dict(width=3))
    return fig

def create_department_distribution_chart(student_data):
    """
    Generates a Plotly Donut (pie) chart depicting student department distribution.
    """
    if not student_data:
        fig = go.Figure()
        fig.update_layout(
            title="No Student Data Available",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

    df = pd.DataFrame(student_data)
    dept_counts = df["department"].value_counts().reset_index()
    dept_counts.columns = ["Department", "Students"]

    fig = px.pie(
        dept_counts, 
        values="Students", 
        names="Department", 
        hole=0.4,
        title="Student Distribution by Department",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def create_student_growth_chart(student_data):
    """
    Generates a Plotly Bar/Area chart depicting registration growth over years.
    """
    if not student_data:
        fig = go.Figure()
        fig.update_layout(
            title="No Growth Data Available",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        return fig

    df = pd.DataFrame(student_data)
    growth = df.groupby("enrollment_year").size().reset_index(name="Enrollments")
    
    fig = px.bar(
        growth, 
        x="enrollment_year", 
        y="Enrollments",
        title="Student Registrations by Year",
        color="Enrollments",
        color_continuous_scale=px.colors.sequential.Sunsetdark
    )
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(15, 23, 42, 0.4)",
        xaxis=dict(showgrid=False, title="Academic Year", type="category"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="New Enrollments"),
        margin=dict(l=40, r=40, t=50, b=40),
        coloraxis_showscale=False
    )
    return fig
