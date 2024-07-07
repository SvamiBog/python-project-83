import os
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
from datetime import datetime


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


class Database:
    def __enter__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cur = self.conn.cursor(cursor_factory=extras.RealDictCursor)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cur.close()
        self.conn.close()


def get_url_by_id(conn, id):
    with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
        cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
        result = cur.fetchone()
    return result['name'] if result else None


def fetch_and_parse_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return {
                'title': soup.find('title').text if soup.find('title') else None,
                'h1': soup.find('h1').text if soup.find('h1') else None,
                'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None,
                'status_code': response.status_code
            }
        else:
            return {'error': 'Произошла ошибка при проверке'}
    except requests.RequestException:
        return {'error': 'Произошла ошибка при проверке'}


def insert_url_check(conn, url_id, data):
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at) '
            'VALUES (%s, %s, %s, %s, %s, %s)',
            (url_id, data['status_code'], data['h1'], data['title'], data['description'], datetime.now())
        )
        conn.commit()


def check_url_exists(conn, url):
    with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
        cur.execute('SELECT id FROM urls WHERE name = %s', (url,))
        return cur.fetchone()


def insert_new_url(conn, url):
    with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
        cur.execute('INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id', (url, datetime.now()))
        conn.commit()
        return cur.fetchone()['id']


def get_all_urls():
    with Database() as db:
        db.cur.execute('''
            SELECT u.id, u.name, MAX(c.created_at) AS last_checked, MAX(c.status_code) AS last_status_code
            FROM urls u
            LEFT JOIN url_checks c ON u.id = c.url_id
            GROUP BY u.id
            ORDER BY u.created_at DESC
        ''')
        return db.cur.fetchall()


def get_url_details(url_id):
    with Database() as db:
        db.cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
        url_data = db.cur.fetchone()
        db.cur.execute('SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC', (url_id,))
        checks = db.cur.fetchall()
    return url_data, checks
