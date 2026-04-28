import requests
import json

PROJECT_REF = "vspcuryzdspvehxeanzr"
SERVICE_KEY = "sb_secret_MJoGok4NRfX8bD1jnqx1kg_OHltfpZf"

SQL = """
CREATE TABLE IF NOT EXISTS leads (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  name text NOT NULL,
  phone text NOT NULL,
  email text NOT NULL,
  query text NOT NULL,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS admin_users (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  username text UNIQUE NOT NULL,
  password_hash text NOT NULL
);
"""

def create_tables():
    url = f"https://api.supabase.com/v1/projects/{PROJECT_REF}/database/query"
    headers = {
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"query": SQL})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 200:
        print("\n✅ Tables created successfully!")
    else:
        print("\n❌ Failed. Check the error above.")

if __name__ == "__main__":
    create_tables()
