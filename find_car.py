import requests
from bs4 import BeautifulSoup as Bs
import re

def search_car_by_num(num: str):
    url = f'https://baza-gai.com.ua/nomer/{num}'
    res = requests.get(url)
    print(res.status_code)
    text = res.text
    parser = Bs(text, 'lxml')
    try:
        container = parser.find_all('small')[1].text
    except IndexError:
        return 'Sorry, I cant find it(', False
    result = str(container)
    result = ''.join(re.findall(r'[^()]', result))
    result = ''.join(re.findall(r'связан с .+', result))
    result = result.split(' ')[2::]
    color = result[0]
    brand = result[1]
    model = result[2]
    try:
        year = result[3]
        pretty_str = f'numer => {num}\ncolor => {color}\nbrand => {brand}\nmodel => {model}\nyear => {year}'
    except IndexError:
        year = result[-1]
        pretty_str = f'numer => {num}\ncolor => {color}\nbrand => {brand}\nmodel => {model}\nyear => {year}'
    print(result)

    return pretty_str, True


