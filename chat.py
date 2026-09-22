import streamlit as st
from google import genai
from google.genai import types
import random
import time

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="ZuuZuu Healthcare Assistant",
    page_icon="🩺",
    layout="wide"
)

API_KEY = "YOUR_GEMINI_API_KEY"

# =====================================
# CUSTOM CSS
# =====================================

st.markdown("""
<style>

.stApp{
background: linear-gradient(
135deg,
#f5f7fa,
#e0f7fa,
#ffffff
);
}

.main-title{
text-align:center;
font-size:55px;
font-weight:bold;
color:#009688;
}

.subtitle{
text-align:center;
font-size:18px;
color:gray;
margin-bottom:20px;
}

.card{
background:white;
padding:20px;
border-radius:20px;
box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}

</style>
""", unsafe_allow_html=True)

# =====================================
# START SCREEN
# =====================================

if "started" not in st.session_state:
    st.session_state.started = False

if not st.session_state.started:

    st.markdown("""
    <div class="main-title">🩺 ZuuZuu</div>
    <div class="subtitle">
    Your Friendly Healthcare Assistant
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### Welcome

    Ask healthcare-related questions and receive educational guidance.

    #### Features

    ✅ AI Healthcare Chat

    ✅ BMI Calculator

    ✅ Water Intake Calculator

    ✅ Quick Health Questions

    ✅ Emergency Detection

    ✅ Download Chat History
    """)

    if st.button("🚀 Start Chatting", use_container_width=True):
        st.session_state.started = True
        st.rerun()

    st.stop()

# =====================================
# SYSTEM PROMPT
# =====================================

SYSTEM_PROMPT = """
You are ZuuZuu, a friendly Healthcare Information Assistant.

Rules:
- Answer only healthcare related questions.
- Provide educational health information.
- Do not diagnose diseases.
- Do not prescribe medicines.
- Recommend consulting healthcare professionals.
- For emergencies advise immediate medical attention.
- Use friendly and simple language.
"""

# =====================================
# HEADER
# =====================================

st.markdown(
"""
<div class="main-title">
🩺 ZuuZuu
</div>
<div class="subtitle">
Your AI Healthcare Assistant
</div>
""",
unsafe_allow_html=True
)

# =====================================
# SESSION
# =====================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🩺 ZuuZuu")

    st.success("AI Healthcare Assistant")

    st.divider()

    st.subheader("👤 Profile")

    name = st.text_input("Name")

    age = st.number_input(
        "Age",
        min_value=1,
        max_value=120,
        value=25
    )

    st.divider()

    st.subheader("🏃 BMI Calculator")

    weight = st.number_input(
        "Weight (kg)",
        min_value=1.0,
        value=60.0
    )

    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        value=170.0
    )

    if st.button("Calculate BMI"):

        bmi = weight / ((height/100)**2)

        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        st.success(f"BMI: {bmi:.2f}")
        st.info(f"Category: {category}")

    st.divider()

    st.subheader("💧 Water Intake")

    water = weight * 0.033

    st.success(
        f"Recommended: {water:.1f} Litres/Day"
    )

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.warning(
        """
        Disclaimer:

        ZuuZuu provides health information only.

        It is NOT a replacement for a doctor.
        """
    )

# =====================================
# DASHBOARD
# =====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💬 Messages",
        len(st.session_state.messages)
    )

with col2:
    st.metric(
        "⚡ AI Status",
        "Online"
    )

with col3:
    st.metric(
        "🏃 BMI Tool",
        "Ready"
    )

with col4:
    st.metric(
        "💧 Water Tool",
        "Ready"
    )

st.divider()

# =====================================
# HEALTH TIPS
# =====================================

health_tips = [
    "🚶 Walk for at least 30 minutes daily.",
    "💧 Drink enough water throughout the day.",
    "🥗 Eat more fruits and vegetables.",
    "😴 Get 7-8 hours of sleep.",
    "🏃 Exercise regularly.",
    "🧘 Manage stress through meditation."
]

st.info(random.choice(health_tips))

# =====================================
# QUICK QUESTIONS
# =====================================

st.subheader("⚡ Quick Questions")

c1, c2, c3, c4 = st.columns(4)

with c1:
    if st.button("🥗 Healthy Diet"):
        st.session_state.auto_question = (
            "Suggest a healthy vegetarian diet plan"
        )

with c2:
    if st.button("🏃 Fitness Tips"):
        st.session_state.auto_question = (
            "Give me daily fitness tips"
        )

with c3:
    if st.button("😴 Better Sleep"):
        st.session_state.auto_question = (
            "How can I improve my sleep quality?"
        )

with c4:
    if st.button("💧 Hydration"):
        st.session_state.auto_question = (
            "Benefits of drinking enough water"
        )

# =====================================
# CHAT DISPLAY
# =====================================

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =====================================
# INPUT
# ===