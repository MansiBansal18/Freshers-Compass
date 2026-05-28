import streamlit as st
import requests

# --- 1. THE BRAIN (Confirmed Gemini 3 Flash) ---
def get_ai_response(prompt):
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        st.error("Secret Key missing in .streamlit/secrets.toml")
        return None

    # DIRECT PATH TO GEMINI 3 FLASH
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}"
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1000}
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        return data['candidates'][0]['content']['parts'][0]['text']
    except Exception:
        return "The Compass is spinning! Make sure your API key is valid for Gemini 3."

# --- 2. THE PREMIUM LOOK ---
st.set_page_config(page_title="Fresher's Compass", page_icon="🧭", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #E0E0E0; }
    .main-title { color: #E0B0FF; text-align: center; font-size: 3.5rem; font-weight: 800; text-shadow: 0px 0px 10px #E0B0FF; }
    .quote { text-align: center; font-style: italic; color: #A0A0A0; font-size: 1.2rem; }
    .stButton>button {
        background: linear-gradient(90deg, #D8BFD8, #E0B0FF);
        color: black; border-radius: 15px; font-weight: bold; border: none; height: 3.5rem; width: 100%;
    }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0px 5px 15px #E0B0FF; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE LOGIC ---
if 'domain' not in st.session_state:
    st.session_state.domain = ""

if not st.session_state.domain:
    # LANDING PAGE
    st.markdown("<h1 class='main-title'>🧭 Fresher's Compass</h1>", unsafe_allow_html=True)
    st.markdown("<p class='quote'>\"Your first step into the future starts here.\"</p>", unsafe_allow_html=True)
    
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        user_input = st.text_input("", placeholder="What skill do you want to conquer?")
        if st.button("Generate My Path"):
            if user_input:
                st.session_state.domain = user_input
                st.balloons() # CELEBRATION!
                st.rerun()
else:
    # DASHBOARD PAGE
    domain_name = st.session_state.domain.title()
    st.markdown(f"<h1 class='main-title'>Decoding {domain_name}</h1>", unsafe_allow_html=True)
    
    if st.button("⬅ Search Another Skill"):
        st.session_state.domain = ""
        st.rerun()

    st.write("---")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🚀 Pro Roadmap (Verified)")
        if st.button(f"Get {domain_name} Links"):
            st.snow() # Subtle cool effect for roadmap
            with st.spinner("Finding Coursera & YouTube experts..."):
                prompt = f"""Act as a career mentor. Provide a 4-step roadmap for {domain_name}.
                For each step:
                1. Give it a 'Level Up' name.
                2. Suggest ONLY ONE verified course link from Coursera, Udemy, or a high-authority YouTube channel.
                3. Use bullet points, no long paragraphs."""
                st.markdown(get_ai_response(prompt))

    with col2:
        st.subheader("💡 Build Challenge")
        if st.button("Generate Project"):
            with st.spinner("Creating your portfolio piece..."):
                prompt = f"""Suggest ONE real-world project for a student starting {domain_name}.
                Structure:
                - **Concept**: The big idea.
                - **Tech Stack**: List 3 specific tools.
                - **The Build**: 3 step-by-step phases to finish it."""
                st.info(get_ai_response(prompt))