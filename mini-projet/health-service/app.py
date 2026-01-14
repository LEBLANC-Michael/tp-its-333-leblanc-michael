from flask import Flask, request, jsonify
import requests, jwt
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

SECRET_KEY = "secret123"
PERSON_SERVICE_URL = "http://person-service:5001/persons"

health_data = {}

# -------------------
# Utils
# -------------------
def check_token(req):
    auth = req.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        return False
    token = auth.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return True
    except:
        return False

def person_exists(pid):
    try:
        r = requests.get(f"{PERSON_SERVICE_URL}/{pid}")
        return r.status_code == 200
    except:
        return False

# -------------------
# Routes
# -------------------
@app.route("/health/<int:pid>", methods=["POST"])
def add_health(pid):
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    if not person_exists(pid):
        return jsonify({"error": "Person not found"}), 404

    data = request.json

    health_data[pid] = {
        "weight": data.get("weight"),
        "height": data.get("height"),
        "heart_rate": data.get("heart_rate"),
        "blood_pressure": data.get("blood_pressure")
    }

    return jsonify({
        "person_id": pid,
        **health_data[pid]
    })

@app.route("/health/<int:pid>", methods=["GET"])
def get_health(pid):
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    if pid not in health_data:
        return jsonify({"error": "No data"}), 404

    return jsonify({
        "person_id": pid,
        **health_data[pid]
    })

@app.route("/health/<int:pid>", methods=["PUT"])
def update_health(pid):
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    if pid not in health_data:
        return jsonify({"error": "No data"}), 404

    data = request.json
    health_data[pid] = {
        "weight": data.get("weight"),
        "height": data.get("height"),
        "heart_rate": data.get("heart_rate"),
        "blood_pressure": data.get("blood_pressure")
    }

    return jsonify({
        "person_id": pid,
        **health_data[pid]
    })

@app.route("/health/<int:pid>", methods=["DELETE"])
def delete_health(pid):
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 401

    health_data.pop(pid, None)
    return jsonify({"message": "deleted"})

# -------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
