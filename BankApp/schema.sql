-- Suppression des tables existantes si elles existent
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS transactions;

-- Création de la table des utilisateurs
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Création de la table des comptes bancaires
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    account_number TEXT UNIQUE NOT NULL,
    account_type TEXT NOT NULL,
    balance REAL NOT NULL DEFAULT 0.0,
    currency TEXT NOT NULL DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Création de la table des transactions
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_account_id INTEGER NOT NULL,
    receiver_account_id TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_account_id) REFERENCES accounts (id)
);

-- Insertion de quelques utilisateurs de test
INSERT INTO users (username, password, full_name, email, phone, address) VALUES
('user1', 'password', 'Jean Dupont', 'jean.dupont@example.com', '+33123456789', '1 Rue de la Paix, Paris'),
('user2', 'password', 'Marie Martin', 'marie.martin@example.com', '+33987654321', '23 Avenue des Champs-Élysées, Paris');

-- Insertion de comptes bancaires de test
INSERT INTO accounts (user_id, account_number, account_type, balance, currency) VALUES
(1, 'FR7630001007941234567890185', 'Compte Courant', 10000.00, 'EUR'),
(1, 'FR7630001007941234567890186', 'Compte Épargne', 50000.00, 'EUR'),
(2, 'FR7630001007941234567890187', 'Compte Courant', 15000.00, 'EUR');

-- Insertion de quelques transactions de test
INSERT INTO transactions (sender_account_id, receiver_account_id, amount, description, timestamp) VALUES
(1, 'FR7630001007941234567890187', 1200.00, 'Remboursement prêt', datetime('now', '-5 days')),
(3, 'FR7630001007941234567890185', 800.00, 'Facture consultant', datetime('now', '-3 days')),
(1, 'FR7630001007941234567890186', 5000.00, 'Épargne mensuelle', datetime('now', '-1 day'));
