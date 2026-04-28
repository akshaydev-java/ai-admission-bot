import os
from supabase import create_client, Client
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

_supabase_client: Client = None

def _get_secret(key: str, default: str = "") -> str:
    """Read from Streamlit secrets (cloud) or .env (local)."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

def get_db_client() -> Client:
    """Return a Supabase client instance (singleton)."""
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client
    try:
        url = _get_secret("SUPABASE_URL")
        key = _get_secret("SUPABASE_KEY")
        if not url or not key:
            print("Supabase credentials not set.")
            return None
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None

def initialize_database():
    """Check Supabase connection on startup."""
    client = get_db_client()
    if client:
        print("Supabase connected successfully.")
    else:
        print("Supabase connection failed. Check credentials.")

def insert_lead(name, phone, email, query):
    """Insert a new student lead into the leads table."""
    client = get_db_client()
    if client:
        try:
            data = {
                "name": name,
                "phone": phone,
                "email": email,
                "query": query,
                "created_at": datetime.utcnow().isoformat()
            }
            result = client.table("leads").insert(data).execute()
            return len(result.data) > 0
        except Exception as e:
            print(f"Error inserting lead: {e}")
            return False
    return False

def get_all_leads():
    """Fetch all leads ordered by newest first."""
    client = get_db_client()
    if client:
        try:
            result = client.table("leads").select("*").order("created_at", desc=True).execute()
            return result.data
        except Exception as e:
            print(f"Error fetching leads: {e}")
    return []
