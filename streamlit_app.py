import streamlit as st
import requests

st.set_page_config(page_title="AI Sales Chatbot", layout="wide")
st.title("🤖 AI Sales & Customer Engagement Chatbot")
st.write("Chat with our AI bot for inquiries, support, and sales automation.")

user_message = st.text_input("Your Message:", placeholder="Type here...")
if st.button("Send"):
    if user_message.strip():
        api_url = "http://127.0.0.1:5001/chat"
        payload = {"message": user_message}
        with st.spinner("Processing..."):
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                bot_reply = data.get("response", "No response")
                lead_score = data.get("lead_score", 0)
                
                st.success(f"🤖 Bot: {bot_reply}")
                
                if lead_score > 2:
                    st.warning(f"🔥 High Lead Score ({lead_score})! Potential customer detected.")
            else:
                st.error("Error: Could not get a response!")
    else:
        st.warning("Please enter a message.")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Developed for navAI</p>", unsafe_allow_html=True)