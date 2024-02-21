import json

fichier_texte = "votre_fichier.txt"

# Ouvrir le fichier JSON
with open(fichier_texte, 'r') as f:
    data = f.read()

# Séparer le fichier JSON en lignes
lines = data.split('\n')

# Initialiser une liste pour stocker les mots
words = []

# Parcourir les lignes du fichier JSON
for line in lines:
    # Charger la ligne JSON
    try:
        json_obj = json.loads(line)
    except json.JSONDecodeError:
        continue
    
    # Vérifier si la clé "result" existe
    if "result" in json_obj:
        # Récupérer les mots de la clé "result"
        for item in json_obj["result"]:
            words.append(item["word"])

    # Vérifier si la clé "partial_result" existe
    if "partial_result" in json_obj:
        # Récupérer les mots de la clé "partial_result"
        for item in json_obj["partial_result"]:
            words.append(item["word"])

# Concaténer les mots en une seule chaîne de caractères
result_string = ' '.join(words)

# Afficher la chaîne de caractères résultante
print(result_string)
