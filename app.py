import streamlit as st
import requests
import random

# --- 1. THE BRAIN (Optimized for 1.5 Flash & Single Call) ---
def get_ai_response(prompt):
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return "❌ API Key missing in Settings."
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        # Using Gemini 1.5 Flash for maximum stability
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 429:
            return "🚦 The system is a bit crowded! Please wait 60 seconds and try again."
        
        if response.status_code != 200:
            return f"The Compass is recalibrating (Error {response.status_code}). Please try again."

        data = response.json()
        if 'candidates' in data and data['candidates']:
            return data['candidates'][0]['content']['parts'][0]['text']
        else:
            return "The AI stayed silent. Try a different skill name!"
    except Exception as e:
        return "The Compass is spinning! Check your internet connection."

# --- 2. THE PREMIUM CSS (Animations & Layout) ---
st.set_page_config(page_title="Fresher's Compass", page_icon="🧭", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    @keyframes fadeInSlide {
        0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
        100% { opacity: 1; transform: translateY(0); filter: blur(0); }
    }
    .main-title { 
        color: #E0B0FF; text-align: center; font-size: 3.5rem; font-weight: 800; 
        text-shadow: 0px 0px 15px rgba(224, 176, 255, 0.5);
        animation: fadeInSlide 1.2s ease-out forwards;
    }
    .relatable-quote {
        text-align: center; color: #A0A0A0; font-size: 1.1rem; 
        margin-bottom: 2rem; font-style: italic;
        animation: fadeInSlide 1.8s ease-out forwards;
        animation-delay: 0.3s; opacity: 0;
    }
    .content-card {
        background: rgba(255, 255, 255, 0.05); padding: 22px; border-radius: 18px;
        border: 1px solid rgba(224, 176, 255, 0.15); margin-bottom: 20px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        animation: fadeInSlide 1s ease-in-out;
    }
    .stButton>button {
        background: linear-gradient(90deg, #D8BFD8, #E0B0FF);
        color: black; border-radius: 12px; font-weight: bold; border: none;
        transition: 0.3s; width: 100%; height: 3.5rem;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 20px #E0B0FF; }
    </style>
    """, unsafe_allow_html=True)

QUOTES = [
    "“The expert in anything was once a beginner.”",
    "“Your direction is more important than your speed.”",
    "“Confusion is the first step towards mastery.”",
    "“The best time to start was yesterday. The second best time is now.”"
]

TIPS = [
    "Tip: Consistency beats intensity. 30 mins a day > 5 hours once a week.",
    "Tip: Don't just follow tutorials. Build something that breaks!",
    "Tip: Your LinkedIn is your digital handshake. Keep it professional.",
    "Tip: The best way to learn is to explain it to someone else."
]

# --- 3. THE LOGIC ---
if 'domain' not in st.session_state:
    st.session_state.domain = ""

with st.sidebar:
    st.markdown("### 💡 Daily Compass Tip")
    st.info(random.choice(TIPS))
    st.write("---")
    st.caption("Mansi's Fresher's Compass v2.0")

if not st.session_state.domain:
    # --- PAGE 1: LANDING ---
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='relatable-quote'>{random.choice(QUOTES)}</p>", unsafe_allow_html=True)
    
    user_input = st.text_input("", placeholder="Which skill do you want to master today?")
    if st.button("Unlock My Roadmap"):
        if user_input:
            st.session_state.domain = user_input
            st.balloons()
            st.rerun()
else:
    # --- PAGE 2: DASHBOARD ---
    domain_name = st.session_state.domain.upper()
    st.markdown(f"<h1 class='main-title'>DECODING {domain_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='relatable-quote'>{random.choice(QUOTES)}</p>", unsafe_allow_html=True)

    if st.button("⬅ Search New Skill"):
        st.session_state.domain = ""
        st.rerun()

    st.write("---")

    # SINGLE CALL GENERATION
    with st.spinner(f"Architecting the path for {domain_name}..."):
        # We ask for everything in one prompt to save API quota
        combined_prompt = (
            f"Act as a career mentor. For the skill '{domain_name}':\n"
            f"1. Give a clear 4-step roadmap with ONE famous free resource link for each step.\n"
            f"2. Suggest ONE starter project (Concept, Tech Stack, and 3-step Build process).\n"
            f"Format with bold headings and bullet points."
        )
        final_output = get_ai_response(combined_prompt)
        
        st.markdown(f"<div class='content-card'>{final_output}</div>", unsafe_allow_html=True)
        st.snow() # Snow falls as soon as the full content is ready
