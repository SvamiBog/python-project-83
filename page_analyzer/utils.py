from urllib.parse import urlparse


def format_date(value):
    return value.strftime('%Y-%m-%d %H:%M:%S') if value else ''


def normalize_url(url):
    parsed_url = urlparse(url)
    return f'{parsed_url.scheme}://{parsed_url.netloc}'
