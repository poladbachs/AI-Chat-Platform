from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import spacy
import re

nlp = spacy.load("en_core_web_sm")

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

business_responses = {
    "pricing": "Our pricing starts at $99 per month for small businesses. Custom enterprise plans are available. For more details on our pricing and solutions, please visit <a href='https://navai.ch/#solutions' target='_blank'>this link</a>.",
    "features": "Our AI solutions offer comprehensive automation, including lead qualification, customer support, and AI-powered sales follow-ups. Learn more on our <a href='https://navai.ch/#solutions' target='_blank'>Solutions page</a>.",
    "demo": "We offer a free demo of our AI sales automation. Please check out our <a href='https://navai.ch/#process' target='_blank'>Process page</a> to see how it works.",
    "contact": "You can reach our sales team directly. For contact details, please visit our <a href='https://navai.ch/#contact' target='_blank'>Contact section</a>.",
    "custom_solution": "We provide tailored AI solutions to meet your business needs. Learn more about our custom offerings at <a href='https://navai.ch/#solutions' target='_blank'>this link</a>.",
    "integration": "Our systems integrate seamlessly with your existing CRM and support tools. For more details, please visit <a href='https://navai.ch/#solutions' target='_blank'>this link</a>."
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
        "What's your customer service email", "Where can I get more info", "How can I get in touch"
    ],
    "custom_solution": [
        "Can you build a custom AI solution", "Do you offer customized chatbot development",
        "I need a chatbot for my business", "Can you develop a tailored AI model",
        "Do you build AI solutions for specific industries"
    ],
    "integration": [
        "Can this chatbot integrate with my CRM", "How does it connect with customer databases",
        "Can it work with my website", "Does it support API integration",
        "Can it connect to my sales tools", "Can it integrate with existing systems"
    ]
}

def preprocess_text(text):
    """Normalize text by removing extra punctuation and lowering case."""
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

def detect_intent(user_message):
    """Detects intent using NLP vector similarity matching."""
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
    return best_match if best_score > 0.85 else None

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
    print("Starting AI Sales Chatbot. Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        reply, score = get_response(user_input)
        print(f"Bot: {reply} (Lead Score: {score})")
