import json

fichier_json = "T:\message.txt"

# Ouvrir le fichier JSON
with open(fichier_json, 'r') as f:
    data = f.read()

# Séparer le fichier JSON en lignes
lines = data.split('\n')

# Initialiser une liste pour stocker les chaînes de caractères
strings = []

# Parcourir les lignes du fichier JSON
for line in lines:
    # Charger la ligne JSON
    try:
        json_obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    
    # Vérifier si la clé "text" existe
    if "text" in json_obj:
        # Ajouter la chaîne de caractères à la liste
        strings.append(json_obj["text"])

# Concaténer les chaînes de caractères en une seule chaîne
result_string = ' '.join(strings)

print(strings)
# Afficher la chaîne de caractères résultante
print(result_string)