import streamlit as st
import requests

assert hasattr(st, "chat_message"), "Please upgrade Streamlit to 1.22+"

st.set_page_config(page_title="AI Sales Chatbot", layout="wide")

dark_css = """
<style>
body {
    background-color: #1e1e1e;
    color: #f0f0f0;
}
.block-container {
    padding: 2rem;
}
.chat-message {
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 10px;
}
.chat-message-user {
    background-color: #2c2f33;
}
.chat-message-bot {
    background-color: #242629;
}
.high-lead-score {
    color: #ff5555;
    font-weight: bold;
}
</style>
"""
st.markdown("<br>", unsafe_allow_html=True)
st.image("logo-navai.png", width=200) 

st.title("AI Sales & Customer Engagement Chatbot")
st.write("**Automating Sales Interactions and Qualifying Leads 24/7**")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()

for msg in st.session_state["chat_history"]:
    role = msg["role"]
    content = msg["content"]
    if role == "user":
        with st.chat_message("user"):
            st.markdown(f"<div class='chat-message chat-message-user'>{content}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("assistant"):
            st.markdown(f"<div class='chat-message chat-message-bot'>{content}</div>", unsafe_allow_html=True)

user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state["chat_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f"<div class='chat-message chat-message-user'>{user_input}</div>", unsafe_allow_html=True)

    api_url = "http://127.0.0.1:5001/chat"
    payload = {"message": user_input}
    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            data = response.json()
            bot_reply = data.get("response", "No response")
            lead_score = data.get("lead_score", 0)
            if lead_score > 2:
                bot_reply += f"\n\n<span class='high-lead-score'>High Lead Score: {lead_score}</span>"
            st.session_state["chat_history"].append({"role": "assistant", "content": bot_reply})
            with st.chat_message("assistant"):
                st.markdown(f"<div class='chat-message chat-message-bot'>{bot_reply}</div>", unsafe_allow_html=True)
        else:
            error_msg = f"Error from API (Status {response.status_code})"
            st.session_state["chat_history"].append({"role": "assistant", "content": error_msg})
            with st.chat_message("assistant"):
                st.markdown(f"<div class='chat-message chat-message-bot'>{error_msg}</div>", unsafe_allow_html=True)
    except Exception as e:
        error_msg = f"Exception: {e}"
        st.session_state["chat_history"].append({"role": "assistant", "content": error_msg})
        with st.chat_message("assistant"):
            st.markdown(f"<div class='chat-message chat-message-bot'>{error_msg}</div>", unsafe_allow_html=True)