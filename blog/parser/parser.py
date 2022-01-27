import csv

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

URL = 'https://www.house.kg'
PAGE = '/kupit?page='
UA = UserAgent(verify_ssl=False)


def get_html(url, page=None):
    page = PAGE + str(page)
    get_from_page = url + page
    r = requests.get(get_from_page, headers={'UserAgent': UA.random})
    return r.text


def get_data_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    ads = soup.find('div', class_='listings-wrapper').find_all('div', class_='listing')
    ads_list = []
    for i in ads:
        try:
            ads_list.append(
                {
                    'title': i.find('p', class_='title').get_text(strip=True),
                    'detail_url': URL + i.find('p', class_='title').find('a').get('href'),
                    'price': i.find('div', class_='price').get_text(strip=True),
                    'descriptions': i.find('div', class_='description').get_text(strip=True),
                    'image': i.find('img', class_='temp-auto').get('data-src')
                }
            )
        except:
            'Empty file'

    with open('ads.csv', 'a', newline='', encoding='utf-8') as f:
        for i in ads_list:
            writer = csv.writer(f)
            writer.writerow([v for k, v in i.items()])


if __name__ == '__main__':
    pass
    # for i in range(1, 10 + 1):
    #     html = get_html(URL, page=i)
    #     print(get_data_from_html(html))
