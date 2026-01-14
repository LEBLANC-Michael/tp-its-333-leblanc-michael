from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import jwt

app = Flask(__name__)
CORS(app)

SECRET_KEY = "secret123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

with app.app_context():
    db.create_all()

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

# 🔓 PUBLIC — voir toutes les personnes
@app.route("/persons", methods=["GET"])
def list_persons():
    persons = Person.query.all()
    return jsonify([{"id": p.id, "name": p.name} for p in persons])

# 🔓 PUBLIC — voir une personne
@app.route("/persons/<int:pid>", methods=["GET"])
def get_person(pid):
    p = Person.query.get(pid)
    if not p:
        return jsonify({"error": "Not found"}), 404
    return jsonify({"id": p.id, "name": p.name})

# 🔒 PROTÉGÉ — créer
@app.route("/persons", methods=["POST"])
def create_person():
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    p = Person(name=data["name"])
    db.session.add(p)
    db.session.commit()
    return jsonify({"id": p.id, "name": p.name})

# 🔒 PROTÉGÉ — supprimer
@app.route("/persons/<int:pid>", methods=["DELETE"])
def delete_person(pid):
    if not check_token(request):
        return jsonify({"error": "Unauthorized"}), 401
    p = Person.query.get(pid)
    if not p:
        return jsonify({"error": "Not found"}), 404
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
