import requests
from bs4 import BeautifulSoup


def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text, response.status_code
    except requests.RequestException as e:
        return str(e), None


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title').text if soup.find('title') else ''
    h1 = soup.find('h1').text if soup.find('h1') else ''
    description_tag = soup.find('meta', attrs={'name': 'description'})
    description = description_tag['content'] if description_tag else ''

    return {
        'title': title,
        'h1': h1,
        'description': description
    }


def fetch_and_parse_url(url):
    html, status_code = fetch_url(url)
    if status_code == 200:
        return {**parse_html(html), 'status_code': status_code}
    else:
        return {'error': 'Произошла ошибка при проверке: ' + html}
