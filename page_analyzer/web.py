import requests
from bs4 import BeautifulSoup


def fetch_and_parse_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return {
                'title': soup.find('title').text if soup.find('title') else '',
                'h1': soup.find('h1').text if soup.find('h1') else '',
                'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else '',
                'status_code': response.status_code
            }
        else:
            return {'error': 'Произошла ошибка при проверке'}
    except requests.RequestException:
        return {'error': 'Произошла ошибка при проверке'}
