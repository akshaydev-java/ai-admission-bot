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
    # Courses
    "btech": "We offer B.Tech programs in Computer Science, Electronics, Mechanical, Civil, and Electrical Engineering. Duration is 4 years. Would you like details on fees or admission process?",
    "mtech": "We offer M.Tech programs in various specializations. Admission is based on GATE scores. Contact us for more details!",
    "mba": "Our MBA program is a 2-year full-time course with specializations in Finance, Marketing, HR, and Operations. Intake starts every July.",
    "engineering": "We offer top-ranked Engineering programs in CSE, ECE, ME, CE, and EE. Our placement rate is over 90%. Interested in applying?",
    "computer": "Our Computer Science Engineering (CSE) program is one of the most sought-after courses. It covers AI, Data Science, Cloud, and more!",
    "course": "We offer B.Tech, M.Tech, MBA, BCA, MCA, and B.Sc programs. Each program is industry-aligned with strong placement support.",
    "suggest": "Based on your interest, we'd suggest B.Tech (CSE or ECE) for technology, MBA for management, or B.Sc for science. Want more info on any of these?",
    "college": "Our institution is a premier college offering top programs in Engineering, Management, and Science. We have excellent infrastructure, experienced faculty, and 90%+ placement record!",
    "university": "We are an autonomous university offering UG and PG programs across Engineering, Management, Arts, and Science. Ranked among top 50 in India.",
    # Fees
    "fee": "Fee structure varies by course: B.Tech: ₹1–2 Lakhs/year, MBA: ₹1.5–2.5 Lakhs/year. Scholarships available for merit students!",
    "scholarship": "We offer merit-based scholarships covering up to 50% of tuition fees. Government scholarships (SC/ST/OBC) are also applicable.",
    "payment": "Fees can be paid semester-wise or annually. EMI options are also available. Contact our accounts office for details.",
    # Admission
    "admission": "Admission process: 1) Fill online form 2) Appear for entrance test 3) Interview round 4) Document verification. Next intake: July 2025!",
    "apply": "You can apply online at our website or visit our campus directly. The application process takes about 15 minutes. Want the link?",
    "eligibility": "For B.Tech: 10+2 with Physics, Chemistry, Maths (min 60%). For MBA: Graduation with min 50% + valid CAT/MAT score.",
    "entrance": "We accept JEE Main, State CET, and our own entrance test for B.Tech admissions. MBA admissions are based on CAT/MAT/CMAT scores.",
    "document": "Required documents: 10th & 12th marksheets, transfer certificate, migration certificate, passport photos, and ID proof.",
    # Placement
    "placement": "Our placement record is excellent! 90%+ students placed. Top recruiters include TCS, Infosys, Wipro, Amazon, Google, and 100+ more companies.",
    "salary": "Average package offered is ₹5–8 LPA for B.Tech. Highest package recorded is ₹42 LPA from a top MNC.",
    "job": "We have a dedicated placement cell that conducts mock interviews, resume workshops, and connects students with top companies.",
    # Campus
    "hostel": "We have separate boys' and girls' hostels with modern facilities including Wi-Fi, gym, and mess. Monthly fee approx ₹8,000–12,000.",
    "campus": "Our campus spans 50+ acres with smart classrooms, labs, library, sports facilities, and a medical center.",
    "facility": "Facilities include: Smart classrooms, research labs, 24x7 Wi-Fi, sports complex, cafeteria, hostel, and transport services.",
    # Contact
    "contact": "Reach us at: admissions@ourcollege.edu | +91-XXXXX-XXXXX | Visit: Main Campus Road, City. Office hours: Mon–Sat 9AM–5PM.",
    "location": "Our campus is located in the heart of the city with excellent connectivity by road and metro. Exact address: [College Address].",
    "visit": "You are welcome to visit our campus any weekday between 10AM–4PM. Call us to schedule a guided tour!",
    "hello": "Hello! Welcome to our Admission Portal. I can help you with courses, fees, admission process, placements, and more. What would you like to know?",
    "hi": "Hi there! I'm your admission counselor. Ask me anything about our courses, fees, or how to apply!",
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
