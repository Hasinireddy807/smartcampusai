import os
from dotenv import load_dotenv

# Load env variables from .env
load_dotenv()

# App Configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
APP_TITLE = "SmartCampusAI"
APP_SUBTITLE = "AI-Powered Smart Campus Dashboard"

# Directory configurations
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# JSON DB Files
USERS_FILE = os.path.join(DATABASE_DIR, "users.json")
ACTIVITY_FILE = os.path.join(DATABASE_DIR, "activity.json")
SETTINGS_FILE = os.path.join(DATABASE_DIR, "settings.json")
STUDENTS_FILE = os.path.join(DATABASE_DIR, "students.json") # Custom addition to manage student data
FACULTY_FILE = os.path.join(DATABASE_DIR, "faculty.json") # Custom addition to manage faculty directory
ATTENDANCE_FILE = os.path.join(DATABASE_DIR, "attendance.json") # Custom addition to manage attendance
ANNOUNCEMENTS_FILE = os.path.join(DATABASE_DIR, "announcements.json") # Custom addition for announcements
