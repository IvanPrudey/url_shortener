from flask import Flask
import os
import sqlite3


app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    return connect


def init_db():
    connect = get_db_connection()
    connect.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connect.commit()
    connect.close()


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
