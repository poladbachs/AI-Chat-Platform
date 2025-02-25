![Image](https://github.com/user-attachments/assets/04cba3c4-af46-4534-a55a-9a56f5b8d3ea)
# AI Sales & Customer Engagement Chatbot

## Overview
The **AI Sales & Customer Engagement Chatbot** is a demo multi-turn conversational agent built for sales automation. Tailored for [**navAI**](https://navai.ch) company, this chatbot dynamically engages users, qualifies leads, and guides them to relevant website sections via clickable links. It combines structured business responses with AI-generated fallback using DialoGPT and uses NLP-based intent detection for context-aware replies.

---

## 📺 Demo
![Image](https://github.com/user-attachments/assets/ee4f4108-937e-4051-a2a8-000eb965d05f)

---

## Key Features
- **Dynamic Conversation:**  
  A hybrid solution that combines predefined structured responses with AI-generated replies to handle both targeted sales queries and casual small talk.
- **Intent Detection:**  
  Utilizes Spacy vector similarity to understand diverse phrasings and accurately detect sales intents (e.g., pricing, features, demo, contact).
- **Clickable Responses:**  
  Provides immediate responses with links directing users to relevant navAI modules (Solutions, Process, Contact).
- **Lead Qualification:**  
  Implements a lead scoring mechanism that measures buyer intent through keyword analysis, enhancing conversion potential.
- **Flask API & Streamlit UI:**  
  Integrated via a Flask API and showcased through an elegant, interactive Streamlit dashboard for live demonstrations.

## 📌 How It Works
1. **User Query Processing:**  
   The chatbot preprocesses the user input (removing punctuation, converting to lowercase) and applies NLP-based intent detection.
2. **Structured Response Generation:**  
   If a business intent (e.g., "pricing") is detected, the bot returns a predefined response with clickable links referencing navAI website modules.
3. **Fallback to Conversational AI:**  
   For general or casual queries, DialoGPT generates natural responses, ensuring a smooth and engaging conversation.
4. **Lead Qualification:**  
   The system counts sales-related keywords to assign a lead score, providing a metric of buyer interest.

## Tech Stack
- **Programming Language:** Python
- **NLP & AI Models:** Spacy, DialoGPT (via Transformers and PyTorch)
- **Web Framework:** Flask (for API), Streamlit (for interactive UI)

## 🔧 Setup & Installation

```bash
# Clone the repository
git clone https://github.com/YourUsername/spitch-ai-speech-analytics.git
cd spitch-ai-chat-platform

# Install dependencies
pip install -r requirements.txt

# Then download the Spacy English model
python -m spacy download en_core_web_sm

# Run Flask Backend
python app.py

# Run the Streamlit UI
streamlit run streamlit_app.py
```
