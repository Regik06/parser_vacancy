import time
import json
from bs4 import BeautifulSoup
import requests
from time import sleep
import fake_useragent
from pprint import pprint


def get_links(text1, text2, text3):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url = f'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text={text1+text2+text3}&page=1',
        headers={'user-agent':ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        page_count = int(soup.find('div', attrs={'class':'pager'}).find_all('span', recursive=False)[-1].find('a').find('span').text)
    except:
        return
    for page in range(page_count):
        try:
            data = requests.get(
                url=f'https://spb.hh.ru/search/vacancy?area=1&area=2&search_field=name&search_field=company_name&search_field=description&enable_snippets=true&text={text1+text2+text3}&page={page}',
                headers={'user-agent':ua.random}
            )
            if data.status_code != 200:
                continue
            soup = BeautifulSoup(data.content, 'lxml')
            for a in soup.find_all('a', attrs={'class':'serp-item__title'}):
                yield f"{a.attrs['href'].split('?')[0]}"
        except Exception as e:
            print(f'{e}')
        time.sleep(1)


def get_data(link):
    ua = fake_useragent.UserAgent()
    data = requests.get(
        url=link,
        headers={'user-agent':ua.random}
    )
    if data.status_code != 200:
        return
    soup = BeautifulSoup(data.content, 'lxml')
    try:
        name_vacancy = soup.find(attrs={"class":"bloko-header-section-1"}).text
    except:
        name_vacancy=''
    try:
        salary = soup.find(attrs={'class':'bloko-header-section-2 bloko-header-section-2_lite'}).text.replace('\xa0','')
    except:
        salary=''
    try:
        name_company = soup.find(attrs={'class':'vacancy-company-name'}).text
    except:
        name_company = ''

    try:
        sity = soup.find(attrs={'class':'vacancy-company-redesigned'}).find('p').text.replace('\xa0', '')
    except:
        sity = ''

    vacansy = {
        'link': link,
        'name_vacancy': name_vacancy,
        'salary': salary,
        'sity': sity,
        'name_company': name_company
    }
    return vacansy
if __name__ == '__main__':
    data = []
    for a in get_links('python', 'django', 'flask'):
        data.append(get_data(a))
        time.sleep(1)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)