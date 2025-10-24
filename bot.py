from flask import Flask, request
import requests
import os

TOKEN = os.getenv("BOT_TOKEN")
BOT_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

# --- Utility: store user chat IDs in a simple text file ---
def save_user(chat_id):
    with open("users.txt", "a+") as f:
        f.seek(0)
        users = f.read().splitlines()
        if str(chat_id) not in users:
            f.write(str(chat_id) + "\n")

def get_all_users():
    if not os.path.exists("users.txt"):
        return []
    with open("users.txt") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

# --- Webhook route ---
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return "no message"

    chat_id = data["message"]["chat"]["id"]
    text = data["message"].get("text", "")

    # Save the user if they start the bot
    if text.lower().startswith("/start"):
        save_user(chat_id)
        message = "👋 Hello! You’ve been registered to receive updates."
    else:
        message = f"You said: {text}"

    # Send a reply
    requests.post(BOT_URL, json={"chat_id": chat_id, "text": message})
    return "ok"

# --- Optional route to broadcast a message to all known users ---
@app.route("/broadcast", methods=["POST"])
def broadcast():
    data = request.get_json()
    msg = data.get("text", "Hello everyone!")
    users = get_all_users()
    for uid in users:
        requests.post(BOT_URL, json={"chat_id": uid, "text": msg})
    return f"Message sent to {len(users)} users."

@app.route("/")
def home():
    return "Bot is running and ready!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
