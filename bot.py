from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "no message"
    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")
    requests.post(BOT_URL, json={"chat_id": chat_id, "text": f"You said: {text}"})
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
