import os
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    conn.cursor_factory = extras.DictCursor
    return conn


def open_db_connection():
    conn = get_db_connection()
    cur = conn.cursor()
    return conn, cur


def close_db_connection(conn, cur):
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()


def get_url_by_id(conn, id):
    cur = conn.cursor()
    cur.execute('SELECT name FROM urls WHERE id = %s', (id,))
    result = cur.fetchone()
    cur.close()
    return result['name'] if result else None


def get_all_urls():
    conn, cur = open_db_connection()
    cur.execute('''
        SELECT u.id, u.name, MAX(c.created_at) AS last_checked, MAX(c.status_code) AS last_status_code
        FROM urls u
        LEFT JOIN url_checks c ON u.id = c.url_id
        GROUP BY u.id
        ORDER BY u.created_at DESC
    ''')
    urls_data = cur.fetchall()
    conn.close()
    return urls_data


def get_url_details(url_id):
    conn, cur = open_db_connection()
    cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
    url_data = cur.fetchone()
    cur.execute('SELECT * FROM url_checks WHERE url_id = %s ORDER BY created_at DESC', (url_id,))
    checks = cur.fetchall()
    close_db_connection(conn, cur)
    return url_data, checks
