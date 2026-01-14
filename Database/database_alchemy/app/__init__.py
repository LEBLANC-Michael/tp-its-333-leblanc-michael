from flask import Flask
from .models import init_db

app = Flask(__name__)

# Créer les tables au démarrage
init_db()

from . import views

if __name__ == "__main__":
    app.run(debug=True)
