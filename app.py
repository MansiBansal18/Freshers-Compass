import streamlit as st
import requests
import random

# --- 1. THE BRAIN ---
def get_ai_response(prompt):
    try:
        if "GOOGLE_API_KEY" not in st.secrets:
            return "❌ API Key missing in Settings."
        api_key = st.secrets["GOOGLE_API_KEY"]
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent?key={api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code != 200:
            return "The Compass is recalibrating... please try again in a moment."
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "The Compass is spinning! Check your connection."

# --- 2. CONFIG & PREMIUM DESIGN ---
st.set_page_config(page_title="Fresher's Compass", page_icon="🧭", layout="centered")

# Custom CSS for Animations, Layout, and the Lavender Theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    
    /* Title Animation */
    .main-title { 
        color: #E0B0FF; text-align: center; font-size: 3.5rem; font-weight: 800; 
        text-shadow: 0px 0px 15px rgba(224, 176, 255, 0.5);
        animation: fadeIn 2s;
    }
    
    /* Relatable Quote Style */
    .relatable-quote {
        text-align: center; color: #A0A0A0; font-size: 1.1rem; 
        margin-bottom: 2rem; font-style: italic;
    }

    /* Decorative Card for AI Content */
    .content-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(224, 176, 255, 0.2);
        margin-bottom: 20px;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    
    .stButton>button {
        background: linear-gradient(90deg, #D8BFD8, #E0B0FF);
        color: black; border-radius: 12px; font-weight: bold; border: none;
        transition: 0.3s; width: 100%; height: 3rem;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 0px 20px #E0B0FF; }
    </style>
    """, unsafe_allow_html=True)

# Relatable motivational quotes for freshers
QUOTES = [
    "“The expert in anything was once a beginner.”",
    "“Don't watch the clock; do what it does. Keep going.”",
    "“Your direction is more important than your speed.”",
    "“Confusion is the first step towards mastery.”"
]

TIPS = [
    "Tip: Consistency beats intensity. 30 mins a day > 5 hours once a week.",
    "Tip: Don't just follow tutorials. Build something that breaks!",
    "Tip: Your LinkedIn is your digital handshake. Keep it clean.",
    "Tip: The best way to learn is to explain it to someone else."
]

# --- 3. APP LOGIC ---
if 'domain' not in st.session_state:
    st.session_state.domain = ""

# Sidebar Feature: Daily Career Tip (The "New Feature")
with st.sidebar:
    st.markdown("### 💡 Daily Compass Tip")
    st.info(random.choice(TIPS))
    st.write("---")
    st.caption("Crafted for the next generation of builders.")

if not st.session_state.domain:
    # --- PAGE 1: LANDING ---
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='relatable-quote'>{random.choice(QUOTES)}</p>", unsafe_allow_html=True)
    
    user_input = st.text_input("", placeholder="Enter a skill (e.g. Java, Design, Marketing)...")
    
    if st.button("Generate My Path"):
        if user_input:
            st.session_state.domain = user_input
            st.balloons()
            st.rerun()
else:
    # --- PAGE 2: DASHBOARD ---
    domain_name = st.session_state.domain.upper()
    
    # Header with Motivational Quote right around the 'Decoding' text
    st.markdown(f"<h1 class='main-title'>DECODING {domain_name}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='relatable-quote'>{random.choice(QUOTES)}</p>", unsafe_allow_html=True)

    if st.button("⬅ Change Skill"):
        st.session_state.domain = ""
        st.rerun()

    st.write("---")

    # Layout: Sequential view (cleaner than columns for reading roadmaps)
    
    # SECTION 1: ROADMAP
    st.markdown("### 🚀 The Roadmap")
    with st.spinner(f"Mapping out {domain_name}..."):
        prompt = f"Provide a clear 4-step roadmap for {domain_name}. Include one resource link per step."
        roadmap = get_ai_response(prompt)
        st.markdown(f"<div class='content-card'>{roadmap}</div>", unsafe_allow_html=True)

    # SECTION 2: PROJECT
    st.markdown("### 💡 Your First Project")
    with st.spinner("Brainstorming projects..."):
        prompt = f"Suggest ONE beginner project for {domain_name}. Concept, Tech Stack, and 3-step Build process."
        project = get_ai_response(prompt)
        st.markdown(f"<div class='content-card'>{project}</div>", unsafe_allow_html=True)

    st.success("Success! Focus on one step at a time.")
