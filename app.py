import streamlit as st
import requests
import random
import time

# --- 1. THE BRAIN (Straight to Stable 3.1) ---
def get_ai_response(prompt):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ API Key missing."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # Skipping the crowded 3.5 and going straight to 3.1 Flash-Lite
    # This ensures the fastest response time for your users.
    model_name = "gemini-1.5-flash" # Use 1.5-flash as the most widely available stable fallback if 3.x is hitting 503s
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        # Reduced timeout to keep the app snappy
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        elif response.status_code == 503:
            return "OVERLOADED"
        else:
            return f"ERROR_{response.status_code}"
    except Exception:
        return "CONNECTION_FAILED"

# --- 2. RESTORED PREMIUM UI (Original Layout) ---
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

# RESTORED SIDEBAR
with st.sidebar:
    st.markdown("### 💡 Daily Compass Tip")
    tips = [
        "Tip: Consistency beats intensity. 30 mins a day > 5 hours once a week.",
        "Tip: Don't just follow tutorials. Build something that breaks!",
        "Tip: Your LinkedIn is your digital handshake. Keep it professional."
    ]
    st.info(random.choice(tips))
    st.write("---")
    st.caption("Mansi's Fresher's Compass v4.0")

if 'domain' not in st.session_state:
    st.session_state.domain = ""

if not st.session_state.domain:
    # PAGE 1
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Your AI-powered map to career success.</p>", unsafe_allow_html=True)
    
    u_input = st.text_input("", placeholder="Which skill do you want to master?")
    if st.button("Unlock My Roadmap"):
        if u_input:
            st.session_state.domain = u_input
            st.balloons()
            st.rerun()
else:
    # PAGE 2
    st.markdown(f"<h1 class='main-title'>{st.session_state.domain.upper()}</h1>", unsafe_allow_html=True)
    if st.button("⬅ Search New Skill"):
        st.session_state.domain = ""
        st.rerun()

    # SECTION 1: ROADMAP
    st.markdown("### 🚀 Step-by-Step Roadmap")
    with st.spinner("Decoding the path..."):
        r_prompt = f"Provide a clear 4-step roadmap for learning {st.session_state.domain} with links. Use bold keywords."
        r_output = get_ai_response(r_prompt)
        
        if r_output == "OVERLOADED":
            st.warning("🚦 High traffic on Google's end. Please wait 10 seconds and try again.")
        else:
            st.markdown(f"<div class='content-card'>{r_output}</div>", unsafe_allow_html=True)

    # SECTION 2: PROJECT
    st.markdown("### 🛠️ Build Challenge")
    with st.spinner("Generating project ideas..."):
        p_prompt = f"Suggest ONE starter project for {st.session_state.domain} with a tech stack and 3 build steps."
        p_output = get_ai_response(p_prompt)
        
        if p_output != "OVERLOADED" and "ERROR" not in p_output:
            st.markdown(f"<div class='content-card'>{p_output}</div>", unsafe_allow_html=True)
            st.snow()
