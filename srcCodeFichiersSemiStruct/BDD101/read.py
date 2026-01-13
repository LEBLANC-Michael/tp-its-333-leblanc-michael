import json

# 1. Lire le fichier
with open("data.json", "r") as f:
    data = json.load(f)

# 2. Modifier les coordonnées du premier point
data["features"][0]["geometry"]["coordinates"] = [50.0, 30.0]

# 3. Créer une nouvelle feature (nouveau couple de coordonnées)
new_feature = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [10.0, 5.0]
    },
    "properties": {
        "prop0": "nouvelle valeur"
    }
}

# 4. Ajouter la nouvelle feature à la liste
data["features"].append(new_feature)

# 5. Sauvegarder dans le fichier
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

print("Coordonnées mises à jour et nouveau point ajouté !")
