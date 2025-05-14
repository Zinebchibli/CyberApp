@echo off
echo Initialisation de la base de données pour l'application bancaire...

cd %~dp0
set FLASK_APP=app.py
set FLASK_ENV=development

echo Suppression de l'ancienne base de données (si elle existe)...
if exist bank.db (
    del /f bank.db > nul 2>&1
    if errorlevel 1 (
        echo Erreur: La base de données est utilisée par un autre processus.
        echo Fermez toutes les applications Flask et réessayez.
        pause
        exit /b 1
    )
)

echo Création de la nouvelle base de données...
flask init-db

echo Base de données initialisée avec succès!
echo.
echo Utilisateurs de test créés:
echo - Nom d'utilisateur: user1, Mot de passe: password
echo - Nom d'utilisateur: user2, Mot de passe: password
echo.
echo Vous pouvez maintenant démarrer l'application avec la commande: flask run
pause
