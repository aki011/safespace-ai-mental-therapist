import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/ask"

st.set_page_config(page_title="🧠 SafeSpace Therapist", layout="wide")

st.markdown("""
<style>
.chat-bubble-user {
    background-color: #DCF7C5;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    max-width: 75%;
    float: right;
    clear: both;
}
.chat-bubble-bot {
    background-color: #E9ECFF;
    padding: 12px 16px;
    border-radius: 12px;
    margin: 8px 0;
    max-width: 75%;
    float: left;
    clear: both;
}
.header {
    text-align:center;
    font-size:30px;
    font-weight:700;
    padding:10px;
}
.sub {
    text-align:center;
    color:#555;
    padding-bottom:20px;
}
div.stButton > button {
    background-color: #25D366;
    color: white;
    border-radius: 50%;
    height: 48px;
    width: 48px;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='header'>🧠 SafeSpace – AI Therapist</div>", unsafe_allow_html=True)
st.markdown("<div class='sub'>A gentle space to talk and feel heard</div>", unsafe_allow_html=True)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello, I'm here to listen. How are you feeling today?"}
    ]

# Display Chat
for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>{msg['content']}</div>", unsafe_allow_html=True)

st.write("")

# Input + Send Button
col1, col2 = st.columns([9, 1])

with col1:
    user_input = st.text_area("", placeholder="Type something you're feeling...", key="msg")

with col2:
    send = st.button("➤")

# Send Message
if send and user_input.strip():
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    try:
        response = requests.post(BACKEND_URL, json={"message": user_input})
        bot_message = response.json()["response"]
    except:
        bot_message = "⚠️ Unable to reach backend."

    st.session_state.chat_history.append({
        "role": "assistant",
        "content": bot_message
    })

    st.rerun()

