from flask import Flask, request, jsonify, render_template
import cohere

app = Flask(__name__, template_folder="templates")  # Point Flask to the templates folder
co = cohere.Client("yHQ9Vs97b8lhE70cdLtScNty8ckCrGlBnRSaAWDa")

# Store conversation history temporarily per session
session_memory = {}

@app.route("/")  # Serve the homepage
def index():
    return render_template("index.html")  # Render the frontend

@app.route("/chatbot", methods=["POST"])
def chatbot():
    try:
        data = request.json
        user_id = data.get("user_id", "default")  # Unique identifier for session tracking
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        # Maintain conversation history only during the session
        if user_id not in session_memory:
            session_memory[user_id] = []
        
        session_memory[user_id].append({"role": "user", "content": user_message})
        
        # Get response from Cohere
        response = co.chat(
            message=user_message,
            chat_history=session_memory[user_id]
        )
        bot_reply = response.text
        
        session_memory[user_id].append({"role": "assistant", "content": bot_reply})
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500