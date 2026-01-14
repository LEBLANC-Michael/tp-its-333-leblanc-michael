from flask import render_template, request, redirect
from . import app
from .models import Etudiant, Session

# ===== Routes =====
@app.route("/")
def index():
    session = Session()
    etudiants = session.query(Etudiant).all()
    session.close()
    return render_template("index.html", etudiants=etudiants)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    nom = request.form["nom"]
    adresse = request.form["adresse"]
    pincode = request.form["pincode"]

    session = Session()
    e = Etudiant(nom=nom, adresse=adresse, pincode=pincode)
    session.add(e)
    session.commit()
    session.close()

    return redirect("/")

@app.route("/modifier/<int:id>", methods=["POST"])
def modifier(id):
    adresse = request.form["adresse"]
    pincode = request.form["pincode"]

    session = Session()
    etu = session.query(Etudiant).get(id)
    if etu:
        etu.adresse = adresse
        etu.pincode = pincode
        session.commit()
    session.close()

    return redirect("/")
