from flask import Flask, request, jsonify
import requests
import os
from datetime import datetime

app = Flask(__name__)

# 🔴 তোমার Discord Webhook URL
WEBHOOK_URL = "https://discord.com/api/webhooks/1442137250824585368/kedCGOJbuJenL3b8mIt29b5QP85lth83APo1ja2aKnlPDeJNWiIn2VPri2YUGHB44oAI"

# ✅ Home route for Render test
@app.route("/")
def home():
    return "❤️ FARHAN EXE Discord Welcome Bot Running Successfully!"

# ✅ POST route for sending welcome message
@app.route("/join", methods=["POST"])
def join():
    try:
        data = request.get_json()

        # Check required fields
        if not data or "username" not in data:
            return jsonify({"error": "username missing"}), 400

        username = data["username"]
        avatar = data.get("avatar")
        member_number = data.get("memberNumber", 1)

        # Date & Time formatting
        now = datetime.now()
        date = now.strftime("%b %d, %Y")
        time = now.strftime("%I:%M %p")

        # Send first mention message
        mention_payload = {"content": f"<@{username}>"}
        requests.post(WEBHOOK_URL, json=mention_payload)

        # Embed message structure
        embed_payload = {
            "embeds": [
                {
                    "title": f"❤️ Welcome <@{username}>",
                    "description": (
                        f"Welcome <@{username}> to **FARHAN EXE**\n\n"
                        f"You are our **{member_number}** member.\n\n"
                        f"Checkout:\n"
                        f"🔗 https://discord.com/channels/1344909960441499668/1418979701124497609\n"
                        f"🔗 https://discord.com/channels/1344909960441499668/1345304447961665629\n\n"
                        f"**User <@{username}> Joined At:**\n"
                        f"{date} | {time}"
                    ),
                    "color": 0xFF0000,  # Red separator
                    "thumbnail": {"url": avatar} if avatar else {},
                    "footer": {"text": "Welcome to FARHAN EXE Community ❤️"}
                }
            ]
        }

        # Send final embed message
        r = requests.post(WEBHOOK_URL, json=embed_payload)
        status = "Success" if r.status_code == 204 else f"Failed ({r.status_code})"

        return jsonify({"status": status})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ Flask app run config (Render uses PORT env)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
