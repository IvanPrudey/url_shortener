from flask import Flask
import os
import sqlite3


app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    return connect


if __name__ == '__main__':
    app.run(debug=True)