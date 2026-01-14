from flask import Flask, request, jsonify
import jwt
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

SECRET_KEY = "secret123"

# -------------------
# LOGIN
# -------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # utilisateur simple admin/admin
    if username == "admin" and password == "admin":
        token = jwt.encode(
            {"user": username, "exp": datetime.utcnow() + timedelta(hours=2)},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
