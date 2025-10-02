from flask import Flask, render_template
import os
import random
import string
import sqlite3


CREATE_QUERY = '''
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_url TEXT NOT NULL,
                short_code TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        '''

app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    return connect


def init_db(create_query):
    try:
        with get_db_connection() as connect:
            connect.execute(create_query)
            connect.commit()
            print('База данных успешно инициализирована')
    except Exception as e:
        print(f'Ошибка инициализации базы: {e}')


def generate_short_code():
    length = 6
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters for _ in range(length)))


@app.route('/')
def index():
    return render_template('index.html')


def shorten_url():
    pass


def redirect_to_url():
    pass


if __name__ == '__main__':
    init_db(CREATE_QUERY)
    app.run(debug=True)
