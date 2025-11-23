from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# --------------------------
# 🔴 YOUR WEBHOOK URL HERE
# --------------------------
WEBHOOK_URL = "https://discord.com/api/webhooks/1442137250824585368/kedCGOJbuJenL3b8mIt29b5QP85lth83APo1ja2aKnlPDeJNWiIn2VPri2YUGHB44oAI"


# --------------------------
# Get user avatar (auto fetch)
# --------------------------
def get_user_avatar(user_id):
    try:
        r = requests.get(
            f"https://discord.com/api/v10/users/{user_id}",
            headers={"User-Agent": "DiscordBot"},
            timeout=5
        )
        if r.status_code == 200:
            data = r.json()
            avatar_hash = data.get("avatar")

            if avatar_hash:
                return f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png?size=1024"
            else:
                return f"https://cdn.discordapp.com/embed/avatars/{int(user_id) % 5}.png"

    except:
        pass

    # fallback avatar (discord default)
    return f"https://cdn.discordapp.com/embed/avatars/1.png"


# --------------------------
# Send welcome message
# --------------------------
def send_welcome(user_id, member_number, date, time):
    avatar = get_user_avatar(user_id)

    # First message (mention)
    requests.post(WEBHOOK_URL, json={"content": f"<@{user_id}>"})

    # Second message (embed)
    embed = {
        "embeds": [
            {
                "title": f"❤️ Welcome <@{user_id}>",
                "description": (
                    f"Welcome <@{user_id}> to **FARHAN EXE**\n\n"
                    f"You are our **{member_number}** member.\n\n"
                    f"Checkout:\n"
                    f"🔗 https://discord.com/channels/1344909960441499668/1418979701124497609\n"
                    f"🔗 https://discord.com/channels/1344909960441499668/1345304447961665629\n\n"
                    f"**User <@{user_id}> Joined At:**\n"
                    f"{date} | Yesterday at {time}"
                ),
                "color": 0xFF0000,
                "thumbnail": {"url": avatar},
                "footer": {"text": "Welcome to FARHAN EXE"}
            }
        ]
    }

    requests.post(WEBHOOK_URL, json=embed)


# --------------------------
# API Route
# --------------------------
@app.route("/welcome", methods=["POST"])
def welcome_api():
    data = request.json

    send_welcome(
        user_id=data["userId"],
        member_number=data["memberNumber"],
        date=data["date"],
        time=data["time"]
    )

    return jsonify({"status": "Welcome Sent"})


# --------------------------
# Run (Render uses PORT)
# --------------------------
if __name__ == "__main__":
    import os
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
