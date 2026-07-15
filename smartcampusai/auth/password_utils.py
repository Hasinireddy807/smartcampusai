import bcrypt

def hash_password(password: str) -> str:
    """Hashes a clear text password using bcrypt and returns a UTF-8 string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def check_password(password: str, hashed_password: str) -> bool:
    """Verifies a clear text password against its bcrypt hashed counterpart."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False
