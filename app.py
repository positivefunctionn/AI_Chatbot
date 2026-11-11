
import os
import uuid

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

from chatbot import ChatbotEngine

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY is missing from .env")

chatbot = ChatbotEngine()


@app.route("/")
def home():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())

    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Please enter a message."}), 400

        session_id = session.get("session_id")

        if not session_id:
            return jsonify({
                "error": "Session expired. Refresh the page."
            }), 400

        response = chatbot.get_response(session_id, user_message)

        return jsonify({"response": response})

    except Exception:
        app.logger.exception("Chat request failed")
        return jsonify({
            "error": "Something went wrong. Please try again."
        }), 500


@app.route("/clear", methods=["POST"])
def clear():
    session_id = session.get("session_id")

    if session_id:
        chatbot.clear_conversation(session_id)

    return jsonify({
        "message": "Conversation memory cleared."
    })


if __name__ == "__main__":
    app.run(debug=True)
