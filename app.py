import streamlit as st
import pandas as pd
from datetime import datetime
from db import initialize_database, insert_lead, get_all_leads
from auth import authenticate_admin, create_initial_admin
from chatbot import get_chatbot_response, SYSTEM_PROMPT, generate_auto_replies
import os

# Page Config
st.set_page_config(page_title="AI Admission System", layout="wide", page_icon="🎓")

# Initialize DB on start
initialize_database()
create_initial_admin()

# Session State for Auth
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Session State for Chat
if 'messages' not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your admission counselor. How can I help you today?"}]

# --- Sidebar Navigation ---
st.sidebar.title("🎓 Admission Portal")
page = st.sidebar.radio("Navigation", ["AI Chatbot", "Lead Collection", "Admin Dashboard", "Settings"])

def login_form():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate_admin(username, password):
            st.session_state.authenticated = True
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid credentials.")

if page == "AI Chatbot":
    st.title("💬 AI Admission Counselor")
    st.write("Ask anything about our courses, fees, or admission process.")

    # Display chat messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Quick suggestions
    suggestions = generate_auto_replies(st.session_state.messages)
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        if cols[i].button(suggestion, key=f"suggest_{i}"):
            st.session_state.messages.append({"role": "user", "content": suggestion})
            # Prepare messages for API
            api_msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
            with st.spinner("AI is thinking..."):
                resp = get_chatbot_response(api_msgs)
            st.session_state.messages.append({"role": "assistant", "content": resp})
            st.rerun()

    # Chat Input
    if prompt := st.chat_input("Type your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        api_msgs = [{"role": "system", "content": SYSTEM_PROMPT}] + st.session_state.messages
        with st.spinner("AI is thinking..."):
            response = get_chatbot_response(api_msgs)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

elif page == "Lead Collection":
    st.title("📝 Student Inquiry Form")
    st.write("Please leave your details and we will get back to you.")
    
    with st.form("lead_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email Address")
        query = st.text_area("Your Query")
        submitted = st.form_submit_button("Submit Details")
        
        if submitted:
            if name and phone and email and query:
                if insert_lead(name, phone, email, query):
                    st.success("Thank you! Your inquiry has been submitted.")
                    st.balloons()
                else:
                    st.error("Something went wrong. Please try again.")
            else:
                st.warning("Please fill all fields.")

elif page == "Admin Dashboard":
    if not st.session_state.authenticated:
        login_form()
    else:
        st.title("📊 Admin Dashboard")
        st.write("Manage student leads and inquiries.")
        
        leads = get_all_leads()
        if leads:
            df = pd.DataFrame(leads)
            # Remove MongoDB internal ID for display if preferred, or keep as string
            
            st.metric("Total Leads", len(df))
            
            # Search filter
            search = st.text_input("Search (Name/Email/Phone)")
            if search:
                df = df[df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
            
            st.dataframe(df, use_container_width=True)
            
            # Export
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Leads as CSV",
                data=csv,
                file_name=f'leads_{datetime.now().strftime("%Y%m%d")}.csv',
                mime='text/csv',
            )
        else:
            st.info("No leads found yet.")
        
        if st.sidebar.button("Logout"):
            st.session_state.authenticated = False
            st.rerun()

elif page == "Settings":
    st.title("⚙️ System Settings")
    st.write("Configure your admission system.")
    st.info("Configuration is managed via .env file or environment variables.")
    st.markdown("""
    **Environment Variables:**
    - `OPENAI_API_KEY`: For AI Chatbot
    - `MONGO_URI`: MongoDB connection string
    - `DB_NAME`: Database name (default: admission_db)
    - `DEFAULT_ADMIN_USER`: Initial admin username
    - `DEFAULT_ADMIN_PASS`: Initial admin password
    """)
