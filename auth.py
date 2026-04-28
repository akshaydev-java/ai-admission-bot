import bcrypt
import os
from db import get_db

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    """Checks a password against a bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_admin_user(username: str):
    """Fetch an admin user by username from MongoDB."""
    db = get_db()
    if db is not None:
        try:
            return db.admin_users.find_one({"username": username})
        except Exception as e:
            print(f"Error fetching admin: {e}")
    return None

def create_initial_admin():
    """Create a default admin user if none exists."""
    db = get_db()
    if db is not None:
        try:
            count = db.admin_users.count_documents({})
            if count == 0:
                default_username = os.getenv("DEFAULT_ADMIN_USER", "admin")
                default_password = os.getenv("DEFAULT_ADMIN_PASS", "admin123")
                hashed_pw = hash_password(default_password)
                
                db.admin_users.insert_one({
                    "username": default_username,
                    "password_hash": hashed_pw
                })
                print(f"Default admin created successfully! User: {default_username}")
        except Exception as e:
            print(f"Error creating initial admin: {e}")

def authenticate_admin(username, password):
    """Verify admin credentials."""
    user = get_admin_user(username)
    if user and check_password(password, user['password_hash']):
        return True
    return False
