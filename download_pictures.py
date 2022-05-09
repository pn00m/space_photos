import requests

def download_pictures(url, filename):
    try:
        response = requests.get(url)
        with open(filename, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.ConnectionError:
        pass