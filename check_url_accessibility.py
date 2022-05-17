import requests


def check_url_accessibility(url, payload):
    response = requests.get(url, params=payload)
    response.raise_for_status
    if (response.status_code in (400, 401, 404)) or\
            ('error' in response):
        return None
    return response