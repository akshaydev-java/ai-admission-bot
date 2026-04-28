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
You are a professional admission counselor for a reputed college/institute in India.
Your goal is to help students with their queries regarding:
- Courses offered (B.Tech, M.Tech, MBA, BCA, MCA, B.Sc etc.)
- Fee structures and scholarships
- Admission process and eligibility
- Campus facilities, hostel, placements
- Contact details

Guidelines:
1. Provide short, clear, and human-like answers (2-4 lines max).
2. Be polite, encouraging, and professional.
3. Always answer in the same language the user writes in (Hindi, English, or Hinglish).
4. If asked about specific colleges outside your institution, politely redirect to your own college.
5. Encourage interested users to share their contact details via the Lead form.
"""

FAQ_FALLBACK = {
    "btech": "We offer B.Tech programs in CSE, ECE, ME, CE, and EE. Duration is 4 years. Want details on fees or admission?",
    "mba": "Our MBA is a 2-year program with Finance, Marketing, HR specializations. Intake starts every July.",
    "fee": "B.Tech fees: Rs 1-2 Lakhs/year. Scholarships available for merit students!",
    "admission": "Admission steps: 1) Online form 2) Entrance test 3) Interview 4) Document verification. Next intake: July 2025!",
    "placement": "90%+ placement record. Top recruiters: TCS, Infosys, Amazon, Google and 100+ companies.",
    "contact": "Email: admissions@ourcollege.edu | Call: +91-XXXXX-XXXXX | Mon-Sat 9AM-5PM",
    "hostel": "Separate boys & girls hostels with Wi-Fi, gym, mess. Monthly fee: Rs 8,000-12,000.",
    "scholarship": "Merit scholarships up to 50% tuition. Govt scholarships for SC/ST/OBC also available.",
    "eligibility": "B.Tech: 10+2 with PCM min 60%. MBA: Graduation 50% + CAT/MAT score.",
    "hi": "Hello! I'm your admission counselor. Ask me anything about courses, fees, or admissions!",
    "hello": "Hi there! Welcome to our Admission Portal. How can I help you today?",
}

def _get_groq_client():
    """Create Groq client if API key is available."""
    try:
        from groq import Groq
        api_key = _get_secret("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            return None
        return Groq(api_key=api_key)
    except Exception:
        return None

def get_fallback_response(user_message: str) -> str:
    """Return FAQ fallback response based on keywords."""
    user_message_lower = user_message.lower()
    for key, answer in FAQ_FALLBACK.items():
        if key in user_message_lower:
            return answer
    return "I'd be happy to help! Please ask about our courses, fees, admission process, placements, or facilities. You can also leave your details in the 'Lead Collection' section and we'll contact you!"

def get_chatbot_response(messages: list) -> str:
    """Get AI response from Groq, fallback to FAQ if unavailable."""
    client = _get_groq_client()
    if client is None:
        return get_fallback_response(messages[-1]["content"])
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=200,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Groq API Error: {e}")
        return get_fallback_response(messages[-1]["content"])

def generate_auto_replies(chat_history: list) -> list:
    """Quick reply suggestions."""
    return [
        "What courses do you offer?",
        "What is the fee structure?",
        "How do I apply?"
    ]
