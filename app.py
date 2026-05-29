import streamlit as st
import requests
import random

# --- 1. THE BRAIN (Fixed 404 & Stability) ---
def get_ai_response(prompt):
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return "❌ API Key missing in Settings."
        
        api_key = st.secrets["GOOGLE_API_KEY"]
        # FIXED URL: Using v1beta and the specific model path to avoid 404
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 404:
            return "🧭 Error 404: The Compass lost its map! Please check the API Model name."
        if response.status_code == 429:
            return "🚦 Too many hikers on the trail! Wait 60 seconds and try again."
        if response.status_code != 200:
            return f"⚠️ Compass Glitch (Error {response.status_code}). Try again!"

        data = response.json()
        if 'candidates' in data and data['candidates']:
            return data['candidates'][0]['content']['parts'][0]['text']
        return "The AI stayed silent. Try a different skill!"
    except Exception:
        return "The Compass is spinning! Check your internet."

# --- 2. THE DESIGN (With Highlights) ---
st.set_page_config(page_title="Fresher's Compass", page_icon="🧭", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    .main-title { 
        color: #E0B0FF; text-align: center; font-size: 3.2rem; font-weight: 800; 
        text-shadow: 0px 0px 15px rgba(224, 176, 255, 0.4);
        margin-bottom: 10px;
    }
    .section-header {
        color: #E0B0FF; font-size: 1.8rem; font-weight: 700;
        margin-top: 30px; border-left: 5px solid #E0B0FF; padding-left: 15px;
    }
    .content-card {
        background: rgba(255, 255, 255, 0.05); padding: 20px; border-radius: 15px;
        border: 1px solid rgba(224, 176, 255, 0.2); margin-top: 10px;
        line-height: 1.6;
    }
    .stButton>button {
        background: linear-gradient(90deg, #D8BFD8, #E0B0FF);
        color: black; border-radius: 12px; font-weight: bold; width: 100%; height: 3.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE APP FLOW ---
if 'domain' not in st.session_state:
    st.session_state.domain = ""

if not st.session_state.domain:
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center;'>Your AI-powered map to career success.</p>", unsafe_allow_html=True)
    
    user_input = st.text_input("", placeholder="Enter a skill (e.g. Data Science, UI Design)")
    if st.button("Generate My Roadmap"):
        if user_input:
            st.session_state.domain = user_input
            st.balloons()
            st.rerun()
else:
    # SEARCH PAGE
    st.markdown(f"<h1 class='main-title'>{st.session_state.domain.upper()}</h1>", unsafe_allow_html=True)
    if st.button("⬅ Search Different Skill"):
        st.session_state.domain = ""
        st.rerun()

    with st.spinner("Consulting the experts..."):
        # This prompt tells the AI exactly how to format the "Highlights"
        prompt = (
            f"Act as a mentor for {st.session_state.domain}. "
            f"Provide a structured 4-step roadmap with links and ONE starter project. "
            f"Use Markdown bolding for keywords and sections."
        )
        result = get_ai_response(prompt)
        
        # We split the answer so it's not a big wall of text
        st.markdown("<div class='section-header'>🚀 Your Roadmap</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='content-card'>{result}</div>", unsafe_allow_html=True)
        
        st.snow()
