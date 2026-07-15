import streamlit as st

def render_kpi_card(title, value, subtitle="", icon="📊", color="#6366f1"):
    """
    Renders an aesthetically stunning, modern KPI metric card using glassmorphism.
    """
    st.markdown(
        f"""
        <div class="glass-card metric-container" style="border-left: 4px solid {color}; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div class="metric-label">{title}</div>
                    <div class="metric-value">{value}</div>
                    {f'<div style="font-size: 0.8rem; color: #64748b; margin-top: 0.2rem;">{subtitle}</div>' if subtitle else ''}
                </div>
                <div style="
                    font-size: 1.8rem; 
                    background: rgba(255,255,255,0.04); 
                    padding: 0.5rem; 
                    border-radius: 8px; 
                    border: 1px solid rgba(255,255,255,0.05);
                    line-height: 1;
                ">
                    {icon}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
