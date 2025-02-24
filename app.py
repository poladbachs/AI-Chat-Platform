from flask import Flask, request, jsonify
from chatbot import get_response

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400
    response, lead_score = get_response(message)
    return jsonify({"response": response, "lead_score": lead_score})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)