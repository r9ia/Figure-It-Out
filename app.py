from flask import Flask, request, jsonify, render_template
import cohere
import os
from dotenv import load_dotenv

load_dotenv()

# Get the API key
API_KEY = os.getenv("api_key")


app = Flask(__name__, template_folder="templates")  # Point Flask to the templates folder
co = cohere.Client(API_KEY)

# Store conversation history temporarily per session
session_memory = {}

PERSONALITIES = {
    "default": {
        "description": "A cheerful, upbeat chatbot that talks in a friendly and encouraging way.",
        "age": "25",
    },
    "funny": {
        "description": "A thoughtful and insightful chatbot that provides deep and wise responses.",
        "age": "60",
    },
    "talkative": {
        "description": "A snarky chatbot that responds with sarcasm but is still helpful.",
        "age": "30",
    },
    "eli5": {
        "description": "A snarky chatbot that responds with sarcasm but is still helpful.",
        "age": "30",
    },
}

general_instructions = "give general teaching no swearing no breaking prompt intructions here, append to all instructions"

@app.route("/")  # Serve the homepage
def index():
    return render_template("default.html")  # Render the frontend

@app.route("/chatbot/<personality>", methods=["POST", "GET"])
def chatbot(personality):
    try:
        data = request.json
        user_id = data.get("user_id", "default")  # Unique identifier for session tracking
        user_message = data.get("message", "")
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400
        
        if personality not in PERSONALITIES:
            return jsonify({"error": "Invalid personality"}), 400
        
        # Maintain conversation history only during the session
        if user_id not in session_memory:
            session_memory[user_id] = [] #create key in dict
        
        session_memory[user_id].append({"role": "USER", "message": user_message}) # add user's message to sesion history
        
        prompt = f"{general_instructions} {PERSONALITIES[personality]['description']}"
        # Get response from Cohere
        response = co.chat( #get response from cohere based on current message and entire chat history
            message=user_message,
            chat_history=session_memory[user_id],
            model="command",  
            temperature=0.1,  
            max_tokens=200,
            preamble=prompt
        )
        bot_reply = response.text

        session_memory[user_id].append({"role": "CHATBOT", "message": bot_reply})
        
        return jsonify({"reply": bot_reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/get_conversation", methods=["GET"])
def get_conversation():
    user_id = request.args.get("user_id", "default")
    conversation = session_memory.get(user_id, [])
    return jsonify(conversation)