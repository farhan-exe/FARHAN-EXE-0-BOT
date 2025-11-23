from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

WEBHOOK_URL = "https://discord.com/api/webhooks/1442137250824585368/kedCGOJbuJenL3b8mIt29b5QP85lth83APo1ja2aKnlPDeJNWiIn2VPri2YUGHB44oAI"

@app.route("/")
def home():
    return "FARHAN EXE Discord Welcome Bot Running Successfully!"

@app.route("/join", methods=["POST"])
def join():
    data = request.json
    if not data or "username" not in data:
        return jsonify({"error": "username missing"}), 400

    username = data["username"]
    avatar = data.get("avatar", None)
    member_number = data.get("memberNumber", 1)

    now = datetime.now()
    date = now.strftime("%B %d, %Y")
    time = now.strftime("%I:%M %p")

    embed_data = {
        "content": f"❤️ Welcome <@{username}>",
        "embeds": [
            {
                "title": f"Welcome <@{username}> to FARHAN EXE",
                "description": f"You are our {member_number} member.\n\n"
                               f"Checkout:\n"
                               f"https://discord.com/channels/1344909960441499668/1418979701124497609\n"
                               f"https://discord.com/channels/1344909960441499668/1345304447961665629",
                "color": 16711680,  
                "thumbnail": {"url": avatar} if avatar else {},
                "footer": {
                    "text": f"User <@{username}> Joined At {date} | {time}"
                }
            }
        ]
    }

    response = requests.post(WEBHOOK_URL, json=embed_data)
    return jsonify({"status": "sent", "discord_status": response.status_code})
    

if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
