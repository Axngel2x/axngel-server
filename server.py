from flask import Flask, request, jsonify

app = Flask(__name__)

MASTER_KEY = "AxngelVip"

active_users = {}

@app.route("/")
def home():
    return "Axngel Server Online", 200


@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    user_id = data.get("user_id")
    key = data.get("key")

    if not user_id or not key:
        return jsonify({"status": "error", "msg": "missing fields"}), 400

    if key == MASTER_KEY:
        active_users[user_id] = "vip"
        return jsonify({
            "status": "vip",
            "access": "granted"
        })

    return jsonify({
        "status": "denied",
        "access": "none"
    })


@app.route("/stats", methods=["GET"])
def stats():
    return jsonify({
        "active_users": len(active_users)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)