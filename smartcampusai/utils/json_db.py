import os
import json
import threading
from utils.config import DATABASE_DIR

# Thread lock for safe concurrent writes to JSON files
_db_lock = threading.Lock()

def initialize_database():
    """Ensure database directory and basic JSON files exist with correct default formats."""
    os.makedirs(DATABASE_DIR, exist_ok=True)
    
    defaults = {
        "users.json": [],
        "activity.json": [],
        "settings.json": {"theme": "dark"},
        "students.json": [
            {
                "id": "STU001",
                "name": "Alex Carter",
                "email": "alex.carter@smartcampus.edu",
                "department": "Computer Science",
                "enrollment_year": 2024,
                "status": "Active"
            },
            {
                "id": "STU002",
                "name": "Sarah Jenkins",
                "email": "sarah.j@smartcampus.edu",
                "department": "Data Science",
                "enrollment_year": 2024,
                "status": "Active"
            },
            {
                "id": "STU003",
                "name": "Michael Chang",
                "email": "m.chang@smartcampus.edu",
                "department": "Electrical Engineering",
                "enrollment_year": 2023,
                "status": "Active"
            },
            {
                "id": "STU004",
                "name": "Emily Watson",
                "email": "emily.w@smartcampus.edu",
                "department": "Mechanical Engineering",
                "enrollment_year": 2023,
                "status": "Active"
            },
            {
                "id": "STU005",
                "name": "David Miller",
                "email": "david.m@smartcampus.edu",
                "department": "Business Administration",
                "enrollment_year": 2025,
                "status": "Active"
            }
        ],
        "faculty.json": [
            {
                "id": "FAC001",
                "name": "Dr. Alan Turing",
                "email": "a.turing@smartcampus.edu",
                "department": "Computer Science",
                "designation": "Professor",
                "specialization": "Artificial Intelligence"
            },
            {
                "id": "FAC002",
                "name": "Dr. Grace Hopper",
                "email": "g.hopper@smartcampus.edu",
                "department": "Computer Science",
                "designation": "Associate Professor",
                "specialization": "Compiler Design"
            },
            {
                "id": "FAC003",
                "name": "Dr. Claude Shannon",
                "email": "c.shannon@smartcampus.edu",
                "department": "Electrical Engineering",
                "designation": "Professor",
                "specialization": "Information Theory"
            }
        ],
        "attendance.json": [
            {"date": "2026-07-10", "student_id": "STU001", "status": "Present", "subject": "CS-101"},
            {"date": "2026-07-10", "student_id": "STU002", "status": "Present", "subject": "CS-101"},
            {"date": "2026-07-10", "student_id": "STU003", "status": "Absent", "subject": "EE-102"},
            {"date": "2026-07-10", "student_id": "STU004", "status": "Present", "subject": "EE-102"},
            {"date": "2026-07-11", "student_id": "STU001", "status": "Present", "subject": "CS-102"},
            {"date": "2026-07-11", "student_id": "STU002", "status": "Absent", "subject": "CS-102"},
            {"date": "2026-07-11", "student_id": "STU003", "status": "Present", "subject": "EE-103"},
            {"date": "2026-07-11", "student_id": "STU004", "status": "Present", "subject": "EE-103"},
            {"date": "2026-07-12", "student_id": "STU001", "status": "Present", "subject": "CS-103"},
            {"date": "2026-07-12", "student_id": "STU002", "status": "Present", "subject": "CS-103"},
            {"date": "2026-07-12", "student_id": "STU003", "status": "Present", "subject": "EE-104"},
            {"date": "2026-07-12", "student_id": "STU004", "status": "Absent", "subject": "EE-104"}
        ],
        "announcements.json": [
            {
                "id": 1,
                "title": "Welcome to SmartCampusAI Portal!",
                "content": "We have launched the new AI-powered operations portal. Please explore the AI Assistant and Analytics tab.",
                "date": "2026-07-14",
                "author": "System Admin"
            },
            {
                "id": 2,
                "title": "Midterm Exams Schedule Released",
                "content": "The midterm examinations will start from next Monday. Check the Student tab for detailed timetable schedules.",
                "date": "2026-07-13",
                "author": "Academic Office"
            }
        ]
    }
    
    for filename, default_data in defaults.items():
        filepath = os.path.join(DATABASE_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump(default_data, f, indent=4)
        else:
            # Validate if it is valid JSON
            try:
                with open(filepath, "r") as f:
                    json.load(f)
            except (json.JSONDecodeError, ValueError):
                # Re-write default content on corruption
                with open(filepath, "w") as f:
                    json.dump(default_data, f, indent=4)

# Always initialize directory and structures on import
initialize_database()


def read_json(filepath):
    """Safely reads content from a JSON file, returning empty list/dict on error or missing file."""
    if not os.path.exists(filepath):
        return []
    
    with _db_lock:
        try:
            with open(filepath, "r") as f:
                return json.load(f)
        except Exception:
            return []

def write_json(filepath, data):
    """Safely writes python structure back to a JSON file."""
    with _db_lock:
        try:
            # Write to a temp file first, then replace (atomic write)
            temp_path = filepath + ".tmp"
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=4)
            if os.path.exists(temp_path):
                os.replace(temp_path, filepath)
            return True
        except Exception as e:
            print(f"Error writing to JSON database {filepath}: {e}")
            if os.path.exists(temp_path):
                try: os.remove(temp_path)
                except: pass
            return False

# --- User Management CRUD ---

def find_user(username_or_email, filepath):
    """Finds a user in the JSON user list by username or email (case insensitive)."""
    users = read_json(filepath)
    if not users or not isinstance(users, list):
        return None
    
    query = username_or_email.lower().strip()
    for user in users:
        if user.get("username", "").lower() == query or user.get("email", "").lower() == query:
            return user
    return None

def add_user(user_data, filepath):
    """Appends a new user record. Prevents duplicates on username/email."""
    users = read_json(filepath)
    if not isinstance(users, list):
        users = []
        
    username = user_data.get("username", "").lower().strip()
    email = user_data.get("email", "").lower().strip()
    
    for user in users:
        if user.get("username", "").lower() == username:
            raise ValueError("Username already exists.")
        if user.get("email", "").lower() == email:
            raise ValueError("Email already registered.")
            
    users.append(user_data)
    return write_json(filepath, users)

def update_user(username, updated_fields, filepath):
    """Updates user information by username."""
    users = read_json(filepath)
    if not isinstance(users, list):
        return False
        
    username_lower = username.lower().strip()
    found = False
    for i, user in enumerate(users):
        if user.get("username", "").lower() == username_lower:
            # Update values while keeping static values intact
            for key, val in updated_fields.items():
                if key not in ["username", "email"]:  # Prevent modifying primary keys
                    users[i][key] = val
            found = True
            break
            
    if found:
        return write_json(filepath, users)
    return False

def delete_user(username, filepath):
    """Removes a user by username."""
    users = read_json(filepath)
    if not isinstance(users, list):
        return False
        
    username_lower = username.lower().strip()
    initial_length = len(users)
    users = [u for u in users if u.get("username", "").lower() != username_lower]
    
    if len(users) < initial_length:
        return write_json(filepath, users)
    return False
