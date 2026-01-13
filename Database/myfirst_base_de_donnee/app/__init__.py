from flask import Flask
import os

# Création de l'application Flask
app = Flask(__name__)

# Définir le chemin de la base de données
DB_NAME = os.path.join(os.path.dirname(__file__), "etudiants.db")

# Import des vues après avoir créé app
from . import views

# Initialise la DB au lancement
views.init_db()

if __name__ == "__main__":
    app.run(debug=True)
