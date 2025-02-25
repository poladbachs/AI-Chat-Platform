from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import spacy
import re

nlp = spacy.load("en_core_web_sm")

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

business_responses = {
    "pricing": "Our pricing starts at $99 per month for small businesses. Custom enterprise plans are available.",
    "features": "Our AI chatbot offers lead qualification, customer support automation, and AI-powered sales follow-ups.",
    "demo": "You can book a free demo at our website or contact our sales team for more details.",
    "contact": "You can reach our sales team at contact@navai.ch or visit our contact page.",
}

intent_training_data = {
    "pricing": [
        "How much does it cost", "Tell me about your pricing", "What are the subscription fees",
        "Is there a monthly charge", "What are your plans", "Any discounts available",
        "Tell me pricing details", "How much do I need to pay", "What does it cost"
    ],
    "features": [
        "What features do you offer", "Tell me about the chatbot's capabilities",
        "What functions does this bot have", "What does it do", "How does it help businesses",
        "What services does it provide", "Tell me what it can do"
    ],
    "demo": [
        "Can I book a demo", "Do you offer a trial", "How can I test the chatbot",
        "I want to see how it works", "Can I try it first", "Show me how it works"
    ],
    "contact": [
        "How do I contact you", "How can I reach support", "I need help with something",
        "What’s your customer service email", "Where can I get more info", "How can I get in touch"
    ]
}

def preprocess_text(text):
    """Normalize text by removing extra punctuation and lowering case"""
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

def detect_intent(user_message):
    """Detects intent behind the message using NLP vector similarity matching."""
    processed_message = preprocess_text(user_message)
    doc = nlp(processed_message)
    
    best_match = None
    best_score = 0.0

    for intent, examples in intent_training_data.items():
        for example in examples:
            example_doc = nlp(preprocess_text(example))
            similarity = doc.similarity(example_doc)
            if similarity > best_score:
                best_score = similarity
                best_match = intent

    return best_match if best_score > 0.80 else None

def get_response(message):
    """Processes the user's message and returns an AI-generated or structured response."""

    intent = detect_intent(message)

    if intent:
        return business_responses[intent], 5

    new_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(new_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return response, 0

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply, score = get_response(user_input)
        print(f"Bot: {reply} (Lead Score: {score})")
