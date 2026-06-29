import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = os.path.join(os.path.dirname(__file__), '..', 'spendly.db')


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    db = get_db()
    db.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    NOT NULL UNIQUE,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)
    db.commit()
    db.close()


def seed_db():
    db = get_db()

    count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if count > 0:
        db.close()
        return

    db.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123')),
    )
    db.commit()

    user_id = db.execute("SELECT id FROM users WHERE email = 'demo@spendly.com'").fetchone()['id']

    expenses = [
        (user_id, 850.00,  'Food',          '2026-06-01', 'Monthly groceries'),
        (user_id, 450.00,  'Transport',      '2026-06-04', 'Metro card top-up'),
        (user_id, 1200.00, 'Bills',          '2026-06-06', 'Electricity bill'),
        (user_id, 900.00,  'Health',         '2026-06-09', 'Doctor consultation'),
        (user_id, 649.00,  'Entertainment',  '2026-06-12', 'Netflix subscription'),
        (user_id, 2499.00, 'Shopping',       '2026-06-15', 'New sneakers'),
        (user_id, 300.00,  'Other',          '2026-06-18', 'Stationery'),
        (user_id, 620.00,  'Food',           '2026-06-22', 'Dinner with friends'),
    ]
    db.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        expenses,
    )
    db.commit()
    db.close()
