### Hexlet tests and linter status:
[![Actions Status](https://github.com/SvamiBog/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/SvamiBog/python-project-83/actions) <a href="https://codeclimate.com/github/SvamiBog/python-project-83/maintainability"><img src="https://api.codeclimate.com/v1/badges/7c2880b7e1f63f82903d/maintainability" /></a>



### Demo:
[Demo site](https://python-project-83-c98h.onrender.com/)



   # Page Analyzer

Page Analyzer is a web application built with Flask that allows users to add URLs and analyze them for various attributes like title, h1, and meta description. It uses BeautifulSoup and requests libraries to fetch and parse the content of the pages.

## Features

- Add URLs to the database
- Fetch and display page attributes like title, h1, and description
- Check URLs for updates
- Display the history of checks for each URL

## Requirements

- Python 3.10+
- PostgreSQL
- Flask
- BeautifulSoup
- requests
- dotenv

## Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/SvamiBog/python-project-83.git
    cd python-project-83
    ```

2. **Create a virtual environment and activate it:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database:**
    Ensure you have PostgreSQL installed and create a database for the project.
    ```sql
    CREATE DATABASE page_analyzer;
    ```

    Update the `.env` file with your database credentials:
    ```plaintext
    DATABASE_URL=postgresql://<username>:<password>@localhost/page_analyzer
    SECRET_KEY=<your_secret_key>
    ```

5. **Run the database migrations:**
    ```bash
    python -c "from db import create_tables; create_tables()"
    ```

6. **Run the application:**
    ```bash
    flask run
    ```
    The application will be available at [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Usage

1. **Add a URL:**
    - Enter the URL you want to analyze in the input field on the home page and submit.
    - The URL will be added to the database, and you will be redirected to the URL's detail page.

2. **Check a URL:**
    - On the URL's detail page, click the "Запустить проверку" button to fetch and display the latest attributes of the page.
    - The results of the check will be stored and displayed in a history table.

## Running Tests

To run the tests, use the following command:

```bash
pytest
