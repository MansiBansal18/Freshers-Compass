import streamlit as st
import requests
import random

# --- 1. THE BRAIN (Corrected for 2026 Stable URL) ---
def get_ai_response(prompt):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ API Key missing in Secrets."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # FIXED URL: The "-preview" tag was removed by Google on May 25th.
    # This is the new permanent stable address for the 3.1 Lite model.
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={api_key}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, json=payload, timeout=20)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 404:
            # Automatic fallback if 3.1 isn't available in your specific region yet
            fallback_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            res = requests.post(fallback_url, json=payload, timeout=20)
            if res.status_code == 200:
                return res.json()['candidates'][0]['content']['parts'][0]['text']
            return "404_ERROR"
        elif response.status_code == 503:
            return "OVERLOADED"
        else:
            return f"ERROR_{response.status_code}"
    except Exception:
        return "CONNECTION_FAILED"

# --- 2. THE PREMIUM UI (Exact Original Layout) ---
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

# ORIGINAL SIDEBAR (With Motivational Tips)
with st.sidebar:
    st.markdown("### 💡 Daily Compass Tip")
    TIPS = [
        "Tip: Consistency beats intensity. 30 mins a day > 5 hours once a week.",
        "Tip: Don't just follow tutorials. Build something that breaks!",
        "Tip: Your LinkedIn is your digital handshake. Keep it professional.",
        "Tip: The best way to learn is to explain it to someone else."
    ]
    st.info(random.choice(TIPS))
    st.write("---")
    st.caption("Mansi's Fresher's Compass v5.0")

if 'domain' not in st.session_state:
    st.session_state.domain = ""

if not st.session_state.domain:
    # LANDING PAGE
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Your AI-powered map to career success.</p>", unsafe_allow_html=True)
    
    u_input = st.text_input("", placeholder="Which skill do you want to master today?")
    if st.button("Unlock My Roadmap"):
        if u_input:
            st.session_state.domain = u_input
            st.balloons()
            st.rerun()
else:
    # RESULTS PAGE
    st.markdown(f"<h1 class='main-title'>{st.session_state.domain.upper()}</h1>", unsafe_allow_html=True)
    if st.button("⬅ Search New Skill"):
        st.session_state.domain = ""
        st.rerun()

    # SECTION 1: ROADMAP (Box Highlighted)
    st.markdown("### 🚀 Step-by-Step Roadmap")
    with st.spinner("Decoding the path..."):
        r_output = get_ai_response(f"Provide a clear 4-step roadmap for {st.session_state.domain} with links. Bold keywords.")
        
        if r_output == "OVERLOADED":
            st.warning("🚦 High traffic on Google's end. Please wait 10s and try again.")
        elif r_output == "404_ERROR":
            st.error("🧭 The Compass is having trouble connecting to Google's map. Please check back soon.")
        else:
            st.markdown(f"<div class='content-card'>{r_output}</div>", unsafe_allow_html=True)

    # SECTION 2: PROJECT (Box Highlighted)
    st.markdown("### 🛠️ Build Challenge")
    with st.spinner("Designing a project..."):
        p_output = get_ai_response(f"Suggest ONE starter project for {st.session_state.domain} with tech stack and 3 steps.")
        
        if "ERROR" not in p_output and p_output != "OVERLOADED" and p_output != "404_ERROR":
            st.markdown(f"<div class='content-card'>{p_output}</div>", unsafe_allow_html=True)
            st.snow()
