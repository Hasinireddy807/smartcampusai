import streamlit as st

def init_session():
    """Initializes default Streamlit session state properties."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None
    if "email" not in st.session_state:
        st.session_state.email = None
    if "role" not in st.session_state:
        st.session_state.role = None
    if "fullname" not in st.session_state:
        st.session_state.fullname = None
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"

def login_user(username, email, role, fullname):
    """Establishes login session."""
    st.session_state.authenticated = True
    st.session_state.username = username
    st.session_state.email = email
    st.session_state.role = role
    st.session_state.fullname = fullname

def logout_user():
    """Clears and resets the login session state properties."""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.role = None
    st.session_state.fullname = None
    # Reset other transient values
    if "current_page" in st.session_state:
        del st.session_state["current_page"]
