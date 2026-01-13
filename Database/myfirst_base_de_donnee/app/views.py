from flask import render_template, request, redirect
from . import app
import sqlite3
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "etudiants.db")

# ===== Modèle =====
def init_db():
    """Initialise la base si elle n'existe pas"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS etudiant (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        adresse TEXT,
        pincode TEXT
    )
    """)
    conn.commit()
    conn.close()

def ajouter_etudiant(nom, adresse, pincode):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO etudiant (nom, adresse, pincode) VALUES (?, ?, ?)",
        (nom, adresse, pincode)
    )
    conn.commit()
    conn.close()

def modifier_etudiant(id, adresse, pincode):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "UPDATE etudiant SET adresse=?, pincode=? WHERE id=?",
        (adresse, pincode, id)
    )
    conn.commit()
    conn.close()

def tous_les_etudiants():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM etudiant")
    rows = cur.fetchall()
    conn.close()
    return rows

# ===== Routes / Vues =====
@app.route("/")
def index():
    etudiants = tous_les_etudiants()
    return render_template("index.html", etudiants=etudiants)

@app.route("/ajouter", methods=["POST"])
def ajouter():
    nom = request.form["nom"]
    adresse = request.form["adresse"]
    pincode = request.form["pincode"]
    ajouter_etudiant(nom, adresse, pincode)
    return redirect("/")

@app.route("/modifier/<int:id>", methods=["POST"])
def modifier(id):
    adresse = request.form["adresse"]
    pincode = request.form["pincode"]
    modifier_etudiant(id, adresse, pincode)
    return redirect("/")
