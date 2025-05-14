import sqlite3
from werkzeug.security import generate_password_hash

# Connexion à la base de données
conn = sqlite3.connect('bank.db')
cursor = conn.cursor()

# Création d'un nouveau hachage pour le mot de passe "password"
password = "password"
password_hash = generate_password_hash(password)

print(f"Nouveau hachage généré pour 'password': {password_hash}")

# Mise à jour des mots de passe des utilisateurs dans la base de données
cursor.execute('UPDATE users SET password = ? WHERE username = ?', (password_hash, 'user1'))
cursor.execute('UPDATE users SET password = ? WHERE username = ?', (password_hash, 'user2'))

# Validation des changements et fermeture de la connexion
conn.commit()
conn.close()

print("Mots de passe mis à jour avec succès pour user1 et user2")
