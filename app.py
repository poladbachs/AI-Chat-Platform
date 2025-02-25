from flask import Flask, request, jsonify
from chatbot import get_response

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        if not data or "message" not in data:
            return jsonify({"error": "Invalid input"}), 400
        message = data["message"].strip()
        if not message:
            return jsonify({"error": "Empty message"}), 400
        response, lead_score = get_response(message)
        if not response:
            return jsonify({"error": "No response generated"}), 500
        return jsonify({"response": response, "lead_score": lead_score})
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
