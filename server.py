from flask import Flask, request, jsonify
import time

app = Flask(__name__)

MASTER_CODE = "AxngelVip"

valid_keys = set()
active_users = {}

total_logins = 0


@app.route("/")
def home():
    return "AXNGEL SERVER ONLINE"


# ================= LOGIN =================
@app.route("/login", methods=["POST"])
def login():
    global total_logins

    data = request.json
    user_id = data.get("user_id")
    key = data.get("key")

    if not user_id:
        return jsonify({"status": "error", "msg": "missing user_id"})

    active_users[user_id] = time.time()
    total_logins += 1

    if key == MASTER_CODE:
        return jsonify({"status": "admin"})

    if key in valid_keys:
        return jsonify({"status": "vip"})

    return jsonify({"status": "denied"})


# ================= GENERATE KEY =================
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json

    if data.get("master") == MASTER_CODE:
        new_key = "AXG-" + str(int(time.time()))
        valid_keys.add(new_key)
        return jsonify({"key": new_key})

    return jsonify({"error": "unauthorized"})


# ================= STATS =================
@app.route("/stats")
def stats():
    now = time.time()

    # remove inactive users (30 sec timeout)
    for user in list(active_users):
        if now - active_users[user] > 30:
            del active_users[user]

    return jsonify({
        "active_users": len(active_users),
        "total_logins": total_logins
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)