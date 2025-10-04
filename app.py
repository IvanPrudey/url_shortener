"""
Flask-приложение для создания коротких ссылок.
Позволяет пользователям преобразовывать длинные
url в короткие коды,перенаправлять по коротким
ссылкам и просматривать статус всех созданных ссылок.
Использует SQLite для хранения соответствий между
короткими кодами и оригинальными URL.
"""
from flask import (Flask,
                   flash,
                   redirect,
                   render_template,
                   request)
import os
import random
import string
import sqlite3

from constants_query import (
    CREATE_INDEX_QUERY,
    CREATE_QUERY,
    INSERT_URL_QUERY,
    SELECT_EXISTING_URL_QUERY,
    SELECT_REDIRECT_QUERY,
    SELECT_STATUS_QUERY
)


app = Flask(__name__)
app.secret_key = os.urandom(24)


def get_db_connection():
    """Устанавка соединения с базой данных."""
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    return connect


def init_db(create_query, index_query):
    """Инициализация БД, создание таблицы и индекса."""
    try:
        with get_db_connection() as connect:
            connect.execute(create_query)
            connect.execute(index_query)
            connect.commit()
            print('База данных успешно инициализирована с индексом')
    except Exception as e:
        print(f'Ошибка инициализации базы: {e}')


def generate_short_code():
    """Генерация случайного короткого кода из 6 символов."""
    length = 6
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


@app.route('/')
def index():
    """Отображение главной страницы."""
    return render_template('index.html')


@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Создание короткой ссылки для url."""
    original_url = request.form['url']
    if not original_url:
        flash('Введите url', 'ошибка')
        return redirect('/')
    if not original_url.startswith(('http://', 'https://')):
        original_url = 'https://' + original_url
    connect = get_db_connection()
    try:
        existing_url = connect.execute(
            SELECT_EXISTING_URL_QUERY,
            (original_url,)
        ).fetchone()
        if existing_url:
            short_code = existing_url['short_code']
            short_url = f"{request.host_url}{short_code}"
            flash(
                f'Этот url уже был сокращен ранее! Короткий url: {short_url}',
                'выполнено успешно')
            connect.close()
            return redirect('/')
        short_code = generate_short_code()
        connect.execute(
            INSERT_URL_QUERY,
            (original_url, short_code)
        )
        connect.commit()
        short_url = f"{request.host_url}{short_code}"
        flash(f'Ваш короткий URL: {short_url}', 'выполнено успешно')
    except sqlite3.IntegrityError:
        connect.rollback()
        short_code = generate_short_code()
        try:
            connect.execute(
                INSERT_URL_QUERY,
                (original_url, short_code)
            )
            connect.commit()
            short_url = f"{request.host_url}{short_code}"
            flash(f'Ваш короткий url: {short_url}', 'выполнено успешно')
        except sqlite3.IntegrityError:
            connect.rollback()
            while True:
                short_code = generate_short_code()
                try:
                    connect.execute(
                        INSERT_URL_QUERY,
                        (original_url, short_code)
                    )
                    connect.commit()
                    short_url = f"{request.host_url}{short_code}"
                    flash(
                        f'Ваш короткий URL: {short_url}', 'выполнено успешно')
                    break
                except sqlite3.IntegrityError:
                    connect.rollback()
                    continue
    finally:
        connect.close()
    return redirect('/')


@app.route('/<short_code>')
def redirect_to_url(short_code):
    """Перенаправление по короткому коду на оригинальный url."""
    connect = get_db_connection()
    url_data = connect.execute(
        SELECT_REDIRECT_QUERY, (short_code,)
    ).fetchone()
    connect.close()

    if url_data:
        return redirect(url_data['original_url'])
    else:
        flash('Короткий url не найден')
        return redirect('/')


@app.route('/status')
def get_status():
    """Отображение статуса всех сокращенных ссылок."""
    try:
        with get_db_connection() as connect:
            urls = connect.execute(SELECT_STATUS_QUERY).fetchall()
        return render_template('status.html', urls=urls)
    except Exception as e:
        flash(f'Ошибка при получении статуса: {e}', 'ошибка')
        return redirect('/')


if __name__ == '__main__':
    init_db(CREATE_QUERY, CREATE_INDEX_QUERY)
    app.run(debug=True)
