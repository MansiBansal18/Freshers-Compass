import streamlit as st
import requests
import random
import time

# --- 1. THE BRAIN (Optimized for Gemini 3.x Family) ---
def get_ai_response(prompt):
    if "GOOGLE_API_KEY" not in st.secrets:
        return "❌ API Key missing."
    
    api_key = st.secrets["GOOGLE_API_KEY"]
    
    # We use Gemini 3.5 as primary and 3.1 Flash-Lite as backup
    # These are the current stable models for your 2026 API key
    models = ["gemini-3.5-flash", "gemini-3.1-flash-lite"]
    
    for model_name in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        # We try each model with a quick retry if it's just a temporary 503
        for attempt in range(2):
            try:
                response = requests.post(url, json=payload, timeout=20)
                
                if response.status_code == 200:
                    return response.json()['candidates'][0]['content']['parts'][0]['text']
                
                # If 503 (Server Busy) or 429 (Rate Limit), wait and try again
                if response.status_code in [503, 429]:
                    time.sleep(2)
                    continue
                
                # If 404 or other error, move to the next model in the list
                break
                
            except Exception:
                continue
                
    return "OVERLOADED"

# --- 2. THE UI (Restored & Fixed) ---
st.set_page_config(page_title="Fresher's Compass", page_icon="🧭", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .main-title { color: #E0B0FF; text-align: center; font-size: 3.5rem; font-weight: 800; text-shadow: 0px 0px 15px rgba(224, 176, 255, 0.4); }
    .content-card { background: rgba(255, 255, 255, 0.05); padding: 22px; border-radius: 18px; border: 1px solid rgba(224, 176, 255, 0.15); margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #D8BFD8, #E0B0FF); color: black; border-radius: 12px; font-weight: bold; width: 100%; height: 3.5rem; }
    </style>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🧭 Compass Status")
    st.success("Connected to Gemini 3.x Engine")
    st.info("The Compass now automatically switches to Lite servers if the main trail is busy.")
    st.write("---")
    st.caption("Mansi's Fresher's Compass v3.5")

if 'domain' not in st.session_state:
    st.session_state.domain = ""

if not st.session_state.domain:
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    u_input = st.text_input("", placeholder="Which skill are we decoding today?")
    if st.button("Generate Roadmap"):
        if u_input:
            st.session_state.domain = u_input
            st.balloons()
            st.rerun()
else:
    st.markdown(f"<h1 class='main-title'>{st.session_state.domain.upper()}</h1>", unsafe_allow_html=True)
    if st.button("⬅ Search New"):
        st.session_state.domain = ""
        st.rerun()

    with st.spinner("Finding the most stable connection..."):
        prompt = f"Act as a career mentor. Provide a 4-step roadmap for {st.session_state.domain} with links and one starter project. Bold key words."
        answer = get_ai_response(prompt)
        
        if answer == "OVERLOADED":
            st.error("🚦 Both the Main and Backup Google servers are currently at maximum capacity.")
            st.info("Please wait 30 seconds and click 'Retry' to check for an open slot.")
            if st.button("🔄 Retry"):
                st.rerun()
        else:
            st.markdown(f"<div class='content-card'>{answer}</div>", unsafe_allow_html=True)
            st.snow()
