import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from validators import url as validate_url
from datetime import datetime
from urllib.parse import urlparse

load_dotenv()


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8000)))