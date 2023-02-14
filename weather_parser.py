import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, date, timedelta


def get_temperature_of_day(date=datetime.now().day, 
                           month=datetime.now().month if len(str(datetime.now().month)) == 2 else f'0{datetime.now().month}',
                           year = datetime.now().year,
                           city='київ'
                           ) -> dict:
    if int(date) > 31:
        raise ValueError
    day_id = f'bd{int(date)-int(datetime.now().day)+1}' if int(date)-int(datetime.now().day) > 0 else f'bd{1}'
    url = f'https://ua.sinoptik.ua/погода-{city.lower()}/{year}-{month}-{date}'

    res = requests.get(url)
    if res.status_code > 400:
        raise ValueError('For this date we haven`t got any information')
    text_ = res.text

    parser = bs(text_, 'lxml')
    min_t = parser.find('div', class_ = 'main loaded', id=day_id).find('span').text
    max_t = parser.find('div', class_ = 'main loaded', id=day_id).find_all('span')[1].text
    description = parser.find('div', class_ = 'description').text

    print({'min': min_t, 'max': max_t})
    return {'min': min_t, 'max': max_t}, description

