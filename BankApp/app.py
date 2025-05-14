import os
import sqlite3
import datetime
import json
import requests
from flask import Flask, render_template, redirect, url_for, request, session, g, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'votre_clef_secrete_tres_securisee'
app.config['DATABASE'] = os.path.join(app.root_path, 'bank.db')

# Configuration de la durée de la session
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)

# URL de l'API de surveillance
MONITORING_API_URL = "http://localhost:8001/log"

# Fonction pour obtenir la connexion à la base de données
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

# Fermer la connexion à la base de données à la fin de la requête
@app.teardown_appcontext
def close_db(error):
    if 'db' in g:
        g.db.close()

# Initialisation de la base de données
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode('utf8'))
        db.commit()

# Commande CLI pour initialiser la base de données
@app.cli.command('init-db')
def init_db_command():
    init_db()
    print('Base de données initialisée.')

# Fonction pour envoyer les logs à l'API de surveillance
def send_log(request_data, response_status=200, response_data=None):
    log_data = {
        'timestamp': datetime.datetime.now().isoformat(),
        'client_ip': request.remote_addr,
        'method': request.method,
        'path': request.path,
        'user_agent': request.headers.get('User-Agent', ''),
        'request_data': request_data,
        'response_status': response_status,
        'response_data': response_data
    }
    
    try:
        requests.post(MONITORING_API_URL, json=log_data, timeout=1)
    except requests.exceptions.RequestException:
        # En cas d'erreur, on continue sans bloquer l'application
        app.logger.warning("Impossible d'envoyer les logs à l'API de surveillance")

# Middleware pour vérifier si l'utilisateur est connecté
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

# Route pour la page d'accueil - redirection vers le login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
          # Enregistrer la tentative de connexion
        request_data = {'username': username, 'password': '******'}  # Ne jamais logger les vrais mots de passe
        
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and user['password'] == password:  # Comparaison simple pour le test
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            
            # Envoyer le log de connexion réussie
            send_log(request_data, 200, {'status': 'success', 'message': 'Login successful'})
            
            return redirect(url_for('dashboard'))
        else:
            error = 'Nom d\'utilisateur ou mot de passe incorrect'
            
            # Envoyer le log de connexion échouée
            send_log(request_data, 401, {'status': 'error', 'message': 'Login failed'})
    
    elif request.method == 'GET':
        send_log({}, 200, {'page': 'login'})
    
    return render_template('login.html', error=error)

# Route pour la page de tableau de bord
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    user_id = session.get('user_id')
    
    # Récupérer les informations du compte
    account = db.execute('SELECT * FROM accounts WHERE user_id = ?', (user_id,)).fetchone()
    
    # Récupérer les transactions récentes
    transactions = db.execute('''
        SELECT * FROM transactions 
        WHERE sender_account_id = ? OR receiver_account_id = ? 
        ORDER BY timestamp DESC LIMIT 5
    ''', (account['id'], account['id'])).fetchall()
    
    send_log({}, 200, {'page': 'dashboard', 'user_id': user_id})
    
    return render_template('dashboard.html', 
                           account=account, 
                           transactions=transactions,
                           username=session.get('username'))

# Route pour la page de transfert
@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    db = get_db()
    user_id = session.get('user_id')
    account = db.execute('SELECT * FROM accounts WHERE user_id = ?', (user_id,)).fetchone()
    
    if request.method == 'POST':
        receiver_account = request.form['receiver_account']
        amount = float(request.form['amount'])
        description = request.form['description']
        
        request_data = {
            'receiver_account': receiver_account,
            'amount': amount,
            'description': description
        }
        
        error = None
        
        # Vérifications basiques
        if amount <= 0:
            error = 'Le montant doit être supérieur à 0'
        elif amount > account['balance']:
            error = 'Solde insuffisant'
        else:
            # Dans ce démo, on simule simplement la transaction sans vérifier si le compte destinataire existe
            db.execute('''
                INSERT INTO transactions (sender_account_id, receiver_account_id, amount, description, timestamp)
                VALUES (?, ?, ?, ?, datetime('now'))
            ''', (account['id'], receiver_account, amount, description))
            
            # Mise à jour du solde (seulement pour le compte émetteur dans cette simulation)
            db.execute('UPDATE accounts SET balance = balance - ? WHERE id = ?', (amount, account['id']))
            db.commit()
            
            send_log(request_data, 200, {'status': 'success', 'message': 'Transfer successful'})
            flash('Transfert effectué avec succès!')
            return redirect(url_for('dashboard'))
        
        if error:
            send_log(request_data, 400, {'status': 'error', 'message': error})
            flash(error)
    
    elif request.method == 'GET':
        send_log({}, 200, {'page': 'transfer', 'user_id': user_id})
    
    return render_template('transfer.html', account=account, username=session.get('username'))

# Route pour la page de profil
@app.route('/profile')
@login_required
def profile():
    db = get_db()
    user_id = session.get('user_id')
    
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    send_log({}, 200, {'page': 'profile', 'user_id': user_id})
    
    return render_template('profile.html', user=user, username=session.get('username'))

# Route pour la déconnexion
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    send_log({}, 200, {'status': 'success', 'message': 'Logout', 'user_id': user_id})
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
