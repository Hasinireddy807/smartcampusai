import streamlit as st

def render_footer():
    """
    Renders a premium styled footer at the bottom of the main dashboard screens.
    """
    st.markdown(
        """
        <div class="footer-text">
            SmartCampusAI Operations Portal &copy; 2026. All rights reserved.<br>
            <span style="font-size: 0.75rem; color: rgba(255,255,255,0.15)">
                Version 1.0.0 &bull; Built with Streamlit &amp; Python &bull; Powered by OpenAI
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
