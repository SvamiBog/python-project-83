import os
import validators
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from .web import fetch_and_parse_url
from .db import (Database, get_url_by_id, insert_url_check, check_url_exists,
                 insert_new_url, get_all_urls, get_url_details)
from .url_utils import normalize_url
from .formatting import format_date


load_dotenv()
app = Flask(__name__)
app.jinja_env.filters['date'] = format_date
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')


@app.route('/urls/<int:id>/checks', methods=['POST'])
def create_check(id):
    with Database() as db:
        url = get_url_by_id(db.conn, id)
        if url:
            result = fetch_and_parse_url(url)
            if 'error' not in result:
                insert_url_check(db.conn, id, result)
                flash('Страница успешно проверена', 'alert-success')
            else:
                flash(result['error'], 'alert-danger')
        else:
            flash('URL не найден', 'alert-danger')
    return redirect(url_for('url', id=id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls', methods=['POST'])
def add_url():
    raw_url = request.form['url']
    if not validators.url(raw_url):
        flash('Некорректный URL', 'alert-danger')
        return render_template('index.html'), 422

    normalized_url = normalize_url(raw_url)
    with Database() as db:
        existing_url = check_url_exists(db.conn, normalized_url)
        if existing_url:
            flash('Страница уже существует', 'alert-info')
            return redirect(url_for('url', id=existing_url['id']))
        else:
            try:
                url_id = insert_new_url(db.conn, normalized_url)
                flash('Страница успешно добавлена', 'alert-success')
                return redirect(url_for('url', id=url_id))
            except Exception as e:
                db.conn.rollback()
                flash(f'Произошла ошибка при добавлении URL: {e}', 'alert-danger')
                return render_template('index.html'), 422


@app.route('/urls', methods=['GET'])
def urls():
    urls_data = get_all_urls()
    return render_template('urls.html', urls=urls_data)


@app.route('/urls/<int:id>', methods=['GET'])
def url(id):
    url_data, checks = get_url_details(id)
    return render_template('url.html', url=url_data, checks=checks)
