import os
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_db_client():
    """Establish and return a MongoDB client."""
    try:
        mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
        client = MongoClient(mongo_uri)
        # Force a call to check if connection is successful
        client.admin.command('ping')
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def get_db():
    """Return the admission database instance."""
    client = get_db_client()
    if client:
        db_name = os.getenv("DB_NAME", "admission_db")
        return client[db_name]
    return None

def initialize_database():
    """Ensure collections exist (MongoDB creates them on first insert, but we can set indexes)."""
    db = get_db()
    if db is not None:
        # Create index for admin_users username
        db.admin_users.create_index("username", unique=True)
        print("Database initialized (Collections ready).")

def insert_lead(name, phone, email, query):
    """Insert a new student lead into the leads collection."""
    db = get_db()
    if db is not None:
        try:
            lead_data = {
                "name": name,
                "phone": phone,
                "email": email,
                "query": query,
                "created_at": datetime.utcnow()
            }
            result = db.leads.insert_one(lead_data)
            return True if result.inserted_id else False
        except Exception as e:
            print(f"Error inserting lead: {e}")
            return False
    return False

def get_all_leads():
    """Fetch all leads from the database."""
    db = get_db()
    if db is not None:
        try:
            leads = list(db.leads.find().sort("created_at", -1))
            # Convert ObjectId to string for compatibility with Streamlit/Pandas
            for lead in leads:
                lead["_id"] = str(lead["_id"])
            return leads
        except Exception as e:
            print(f"Error fetching leads: {e}")
    return []
