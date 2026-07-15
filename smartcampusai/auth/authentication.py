import datetime
import streamlit as st
from utils.config import USERS_FILE
from utils.json_db import find_user, add_user
from utils.helper import validate_email, validate_password_strength, log_activity
from utils.session import login_user, logout_user
from auth.password_utils import hash_password, check_password

def register_user(fullname, username, email, password, confirm_password, role):
    """
    Controller function to validate and register a new user in the database.
    """
    fullname = fullname.strip()
    username = username.strip()
    email = email.strip()
    
    if not fullname or not username or not email or not password or not confirm_password:
        return False, "All fields are required."
        
    if password != confirm_password:
        return False, "Passwords do not match."
        
    # Email Validation
    if not validate_email(email):
        return False, "Invalid email format."
        
    # Password Strength Validation
    is_strong, msg = validate_password_strength(password)
    if not is_strong:
        return False, msg
        
    # Check duplicate
    existing_user = find_user(username, USERS_FILE)
    if existing_user:
        return False, "Username is already taken."
        
    existing_email = find_user(email, USERS_FILE)
    if existing_email:
        return False, "Email is already registered."
        
    # Build user record
    hashed = hash_password(password)
    new_user = {
        "fullname": fullname,
        "username": username,
        "email": email,
        "password": hashed,
        "role": role,
        "registration_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        success = add_user(new_user, USERS_FILE)
        if success:
            log_activity(username, "Register Successful", f"Registered as {role}")
            return True, "Registration successful! You can now log in."
        else:
            return False, "Failed to save user to the database."
    except ValueError as ve:
        return False, str(ve)
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

def authenticate_user(username_or_email, password):
    """
    Authenticates user, logs activity, and sets up session.
    """
    username_or_email = username_or_email.strip()
    if not username_or_email or not password:
        return False, "Please fill in all fields."
        
    user = find_user(username_or_email, USERS_FILE)
    if not user:
        log_activity(username_or_email, "Login Failed", "User not found")
        return False, "Invalid username/email or password."
        
    # Verify password
    if check_password(password, user.get("password", "")):
        # Establish session
        login_user(
            username=user.get("username"),
            email=user.get("email"),
            role=user.get("role", "Student"),
            fullname=user.get("fullname")
        )
        log_activity(user.get("username"), "Login Successful", f"Logged in with role: {user.get('role')}")
        return True, "Login successful!"
    else:
        log_activity(user.get("username"), "Login Failed", "Incorrect password")
        return False, "Invalid username/email or password."

def check_auth():
    """
    Authenticates page guards. Returns True if logged in, False otherwise.
    """
    return st.session_state.get("authenticated", False)
