import os
from dotenv import load_dotenv

load_dotenv()

def _get_secret(key: str, default: str = "") -> str:
    """Read from Streamlit secrets (cloud) or .env (local)."""
    try:
        import streamlit as st
        return st.secrets.get(key, os.getenv(key, default))
    except Exception:
        return os.getenv(key, default)

SYSTEM_PROMPT = """
You are a professional admission counselor for our esteemed college/institute.
Your goal is to help students with their queries regarding:
- Courses offered
- Fee structures
- Admission process
- Contact details

Guidelines:
1. Provide short, clear, and human-like answers.
2. Be polite, encouraging, and professional.
3. If asked for something out of scope, politely redirect them to the admission topics.
4. Try to encourage the user to provide their contact details if they seem highly interested.
"""

# Hardcoded FAQ for fallback
FAQ_FALLBACK = {
    "course": "We offer various undergraduate and postgraduate courses in Engineering, Management, and Arts. Please visit our website or provide your contact details for a brochure.",
    "fee": "The fee structure varies by course. On average, it ranges from $5000 to $15000 per year. We also offer scholarships for meritorious students.",
    "admission": "The admission process involves an online application, an entrance test, and an interview round. Our next intake starts in August.",
    "contact": "You can reach us at admissions@ourcollege.edu or call +1-800-555-1234."
}

def _get_openai_client():
    """Lazily create OpenAI client only when a valid key exists."""
    try:
        from openai import OpenAI
        api_key = _get_secret("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            return None
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def get_fallback_response(user_message: str) -> str:
    """Return a fallback response based on keywords if the API fails."""
    user_message_lower = user_message.lower()
    for key, answer in FAQ_FALLBACK.items():
        if key in user_message_lower:
            return answer
    return "I'm currently experiencing some technical difficulties. Please provide your contact details in the 'Leave your Details' section, and our counselors will reach out to you shortly."

def get_chatbot_response(messages: list) -> str:
    """Get response from OpenAI, or fallback to FAQ."""
    client = _get_openai_client()
    if client is None:
        return get_fallback_response(messages[-1]["content"])
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return get_fallback_response(messages[-1]["content"])

def generate_auto_replies(chat_history: list) -> list:
    """Generate quick reply suggestions."""
    return [
        "What courses do you offer?",
        "What is the fee structure?",
        "How do I apply?"
    ]
