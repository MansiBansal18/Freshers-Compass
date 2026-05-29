import streamlit as st
import requests
import random
import time

# --- 1. THE BRAIN (With Automatic Retries) ---
def get_ai_response(prompt):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ API Key missing in Settings."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 2026 STABLE ENDPOINT: Optimized for Gemini 3.5 Flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    # Try 3 times if the API is busy (Error 429)
    for attempt in range(3):
        try:
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            
            if response.status_code == 429:
                time.sleep(2) # Wait 2 seconds and try again
                continue
            
            return f"⚠️ Compass Glitch (Error {response.status_code})"
        except Exception:
            time.sleep(2)
            continue
            
    return "🚦 The trail is too crowded right now. Please refresh in 30 seconds."

# --- 2. THE RESTORED PREMIUM LAYOUT ---
st.set_page_config(page_title="Fresher's Compass", page_icon="🧭", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    .main-title { 
        color: #E0B0FF; text-align: center; font-size: 3.5rem; font-weight: 800; 
        text-shadow: 0px 0px 15px rgba(224, 176, 255, 0.4);
    }
    .content-card {
        background: rgba(255, 255, 255, 0.05); padding: 22px; border-radius: 18px;
        border: 1px solid rgba(224, 176, 255, 0.15); margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(90deg, #D8BFD8, #E0B0FF);
        color: black; border-radius: 12px; font-weight: bold; width: 100%; height: 3.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# SIDEBAR RESTORED
with st.sidebar:
    st.markdown("### 💡 Daily Compass Tip")
    st.info("Tip: Consistency beats intensity. 30 mins a day > 5 hours once a week.")
    st.write("---")
    st.caption("Mansi's Fresher's Compass v2.5")

if 'domain' not in st.session_state:
    st.session_state.domain = ""

if not st.session_state.domain:
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Master any skill with a personalized AI roadmap.</p>", unsafe_allow_html=True)
    
    user_input = st.text_input("", placeholder="What do you want to learn? (e.g., Python, Figma)")
    if st.button("Unlock My Roadmap"):
        if user_input:
            st.session_state.domain = user_input
            st.balloons()
            st.rerun()
else:
    # --- PAGE 2: THE DASHBOARD (Restored Highlights) ---
    st.markdown(f"<h1 class='main-title'>{st.session_state.domain.upper()}</h1>", unsafe_allow_html=True)
    if st.button("⬅ Search New Skill"):
        st.session_state.domain = ""
        st.rerun()

    # ROADMAP SECTION
    st.markdown("### 🚀 Step-by-Step Roadmap")
    with st.spinner("Mapping the route..."):
        roadmap = get_ai_response(f"Provide a clear 4-step roadmap for learning {st.session_state.domain} with links.")
        st.markdown(f"<div class='content-card'>{roadmap}</div>", unsafe_allow_html=True)

    # PROJECT SECTION
    st.markdown("### 🛠️ Hands-on Project")
    with st.spinner("Designing a build challenge..."):
        project = get_ai_response(f"Suggest ONE starter project for {st.session_state.domain} with a tech stack.")
        st.markdown(f"<div class='content-card'>{project}</div>", unsafe_allow_html=True)
        st.snow()
