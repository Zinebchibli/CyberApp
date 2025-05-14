# Application Bancaire de Démonstration (BankApp)

Cette application simule une interface bancaire simple pour la détection de cyberattaques. Elle fait partie du projet plus large "AI-Powered Cyberattack Detection".

## Structure du projet

```
BankApp/
├── app.py                 # Application Flask principale
├── schema.sql             # Schéma de base de données
├── bank.db                # Base de données SQLite (générée)
├── requirements.txt       # Dépendances Python
├── static/                # Fichiers statiques
│   ├── css/               # Feuilles de style
│   └── js/                # Scripts JavaScript
└── templates/             # Templates HTML
    ├── dashboard.html     # Page du tableau de bord
    ├── layout.html        # Template de base
    ├── login.html         # Page de connexion
    ├── profile.html       # Page de profil
    └── transfer.html      # Page de transfert
```

## Installation

1. Clonez ce dépôt
2. Créez un environnement virtuel:
   ```
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```
3. Installez les dépendances:
   ```
   pip install -r requirements.txt
   ```
4. Initialisez la base de données:
   ```
   flask init-db
   ```

## Exécution

```
flask run
```

L'application sera accessible à l'adresse http://localhost:5000

## Comptes de démonstration

- **Nom d'utilisateur**: user1
- **Mot de passe**: password

- **Nom d'utilisateur**: user2
- **Mot de passe**: password

## Fonctionnalités

- **Connexion et authentification**
- **Tableau de bord des comptes**
- **Virements bancaires**
- **Profil utilisateur**

## Communication avec l'API de surveillance

L'application envoie des informations de journalisation à l'API de surveillance à l'adresse `http://localhost:8001/log` pour chaque requête traitée, y compris:

- Horodatage
- Adresse IP du client
- Méthode HTTP
- Chemin d'accès
- Agent utilisateur
- Données de la requête (sans les informations sensibles)
- Code de statut de la réponse
- Données de la réponse

Cette communication permet l'analyse par le système de détection d'attaques.

## Note de sécurité

Cette application est conçue **uniquement à des fins de démonstration** et ne doit pas être utilisée dans un environnement de production. Elle contient intentionnellement des faiblesses de sécurité pour démontrer la détection d'attaques.
