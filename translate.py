import requests
from bs4 import BeautifulSoup as Bs

def translate_from_en_to_ru():
    url = 'https://alerts.in.ua/'
    response = requests.get(url)
    parser = Bs(response.text, 'lxml')
    container = parser.find_all('li', class_ = 'table-row active')
    print(container)

if __name__ == '__main__':
    translate_from_en_to_ru()