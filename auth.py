import bcrypt
import os
from dotenv import load_dotenv
from db import get_db_client

load_dotenv()

def _get_secret(key: str, default: str = "") -> str:
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def get_admin_user(username: str):
    client = get_db_client()
    if client:
        try:
            result = client.table("admin_users").select("*").eq("username", username).execute()
            if result.data:
                return result.data[0]
        except Exception as e:
            print(f"Error fetching admin: {e}")
    return None

def create_initial_admin():
    client = get_db_client()
    if client:
        try:
            result = client.table("admin_users").select("id").execute()
            if len(result.data) == 0:
                default_username = _get_secret("DEFAULT_ADMIN_USER", "admin")
                default_password = _get_secret("DEFAULT_ADMIN_PASS", "admin123")
                hashed_pw = hash_password(default_password)
                client.table("admin_users").insert({
                    "username": default_username,
                    "password_hash": hashed_pw
                }).execute()
                print(f"Default admin created: {default_username}")
        except Exception as e:
            print(f"Error creating initial admin: {e}")

def authenticate_admin(username, password):
    user = get_admin_user(username)
    if user and check_password(password, user['password_hash']):
        return True
    return False
