import streamlit as st
from utils.helper import setup_page, log_activity
from auth.authentication import check_auth
from components.navbar import render_navbar
from components.sidebar import render_sidebar
from components.footer import render_footer
from utils.config import OPENAI_API_KEY, STUDENTS_FILE, FACULTY_FILE, ATTENDANCE_FILE
from utils.json_db import read_json

# 1. Initialize Page Config & Styles
setup_page("AI Assistant")

# 2. Check Authentication Guard
if not check_auth():
    st.warning("🔒 Access denied. Please login first.")
    st.switch_page("app.py")
    st.stop()

# 3. Render Navigation
render_sidebar()
render_navbar()

st.markdown("<h2 class='gradient-text'>Campus AI Assistant</h2>", unsafe_allow_html=True)
st.write("Interact with the SmartCampusAI virtual assistant to query campus operations, analyze student directories, and draft notifications.")

# Check API key existence
api_key_configured = bool(OPENAI_API_KEY.strip())

# Initialize chat messages history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fetch active database statistics for context injection
students_data = read_json(STUDENTS_FILE)
faculty_data = read_json(FACULTY_FILE)
attendance_data = read_json(ATTENDANCE_FILE)

# Construct helper context from database
campus_context = f"""
Campus Database Context (Real-time data):
- Total Students: {len(students_data)}
- Students List: {students_data}
- Total Faculty: {len(faculty_data)}
- Faculty List: {faculty_data}
- Attendance Records: {attendance_data}
"""

if not api_key_configured:
    st.warning(
        "⚠️ **OpenAI API Key is missing!** The AI Assistant is operating in Mock Simulation Mode. "
        "To enable real AI capabilities, configure your `OPENAI_API_KEY` in the `.env` file."
    )

st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
st.markdown("<h4>Ask anything about the campus:</h4>", unsafe_allow_html=True)

# Preset prompt buttons
col_p1, col_p2, col_p3 = st.columns(3)
preset_clicked = None
with col_p1:
    if st.button("📊 Analyze student counts by department"):
        preset_clicked = "Analyze the student counts by department based on current database records."
with col_p2:
    if st.button("📝 Draft a welcome message for faculty"):
        preset_clicked = "Draft a warm professional welcome message for new faculty members joining the Engineering department."
with col_p3:
    if st.button("💡 Suggest ways to improve attendance"):
        preset_clicked = "Based on our student records, suggest 3 practical ways to improve weekly attendance rates."

# Chat container
for chat in st.session_state.chat_history:
    role_label = "👤 **You**" if chat["role"] == "user" else "🤖 **SmartCampusAI**"
    st.markdown(f"{role_label}: {chat['content']}")
    st.markdown("<hr style='margin: 8px 0; border: 0; border-top: 1px solid rgba(255,255,255,0.05);'>", unsafe_allow_html=True)

# Query text box or preset click
query = st.chat_input("Type your question here...")
if preset_clicked:
    query = preset_clicked

if query:
    # 1. Add user query to chat history
    st.session_state.chat_history.append({"role": "user", "content": query})
    st.markdown(f"👤 **You**: {query}")
    
    # Log user query activity
    log_activity(st.session_state.username, "AI Query", f"Question: {query[:60]}...")
    
    # 2. Get AI Response
    with st.spinner("Processing query..."):
        if api_key_configured:
            try:
                import requests
                import json
                
                # Context-rich system prompt
                system_prompt = (
                    "You are the virtual assistant for SmartCampusAI, a premium campus administration dashboard. "
                    "You have direct access to the campus database. Answer queries professionally, accurately, and concisely. "
                    "Here is the current live campus database context:\n"
                    f"{campus_context}"
                )
                
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {OPENAI_API_KEY}"
                }
                
                # Prepare message history
                api_messages = [{"role": "system", "content": system_prompt}]
                for m in st.session_state.chat_history:
                    api_messages.append({"role": m["role"], "content": m["content"]})
                
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": api_messages,
                    "temperature": 0.7
                }
                
                res = requests.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if res.status_code == 200:
                    response_data = res.json()
                    response = response_data["choices"][0]["message"]["content"]
                else:
                    response = f"❌ **API Error ({res.status_code}):** {res.text}"
                
            except Exception as e:
                response = f"❌ **Request failed:** {str(e)}"
        else:
            # Mock responder fallback
            q_lower = query.lower()
            if "department" in q_lower or "student" in q_lower:
                response = (
                    f"🤖 *[Simulation Mode]* There are currently **{len(students_data)} students** in the database. "
                    "The major departments represented include Computer Science, Data Science, Electrical Engineering, and Mechanical Engineering."
                )
            elif "faculty" in q_lower or "welcome" in q_lower:
                response = (
                    "🤖 *[Simulation Mode]* Here is a draft announcement:\n\n"
                    "**Subject: Welcome to the smart campus portal!**\n"
                    "Dear faculty members, we are excited to have you on board with the SmartCampusAI command deck."
                )
            elif "attendance" in q_lower:
                response = (
                    "🤖 *[Simulation Mode]* Based on the attendance log containing "
                    f"**{len(attendance_data)} entries**, you can improve attendance rates by setting automatic alerts, "
                    "encouraging project-based learning, and holding regular feedback sessions."
                )
            else:
                response = (
                    "🤖 *[Simulation Mode]* Hello! I received your query. "
                    "Configure a valid OpenAI API key in your `.env` file to unlock dynamic AI responses."
                )
    
    # 3. Add assistant response to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.markdown(f"🤖 **SmartCampusAI**: {response}")
    st.rerun()

if st.button("🗑️ Clear Conversation History"):
    st.session_state.chat_history = []
    st.toast("Chat history cleared.", icon="🗑️")
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# 8. Render Footer
render_footer()
