from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import spacy

nlp = spacy.load("en_core_web_sm")

model_name = "microsoft/DialoGPT-medium"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

sales_keywords = ["price", "buy", "subscription", "offer", "cost", "discount"]

def get_response(message):
    new_input_ids = tokenizer.encode(message + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(new_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, new_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    doc = nlp(message.lower())
    lead_score = sum(1 for token in doc if token.text in sales_keywords)
    
    return response, lead_score
