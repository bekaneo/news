from bs4 import BeautifulSoup as Soup
from datetime import datetime
import requests
import json

limit = input('Enter how many articles to format or leave blank(15): ') or '15'
date = input('Enter from date or leave blank(2022-07-04): YYYY-MM-DD ') or '2022-07-04'
file_name = input('Enter new file name or leave blank($date_news.json): ') or f'{datetime.now().date()}_news'
url = f"http://newsline.kg/getNews.php?limit={limit}&last_dt={date}%2007:57:33.933739"

response = requests.get(url)
html_page = response.text
news = json.loads(html_page)

if news:
    if news['data']:
        with open(f'{file_name}.json', 'w') as file:
            data = []
            for art in news['data']:
                article = {
                    'id': art['id'],
                    'id_site': art.get('id_site'),
                    'title': art.get('title'),
                    'category': art.get('category'),
                    'category_id': art.get('category_id'),
                    'desc': Soup(art.get('desc'), 'html.parser').text,
                    'dt': art.get('dt'),
                    'img': art.get('img'),
                    'link': art.get('link'),
                    'date': art.get('date'),
                    'site_name': art.get('site_name')
                }
                data.append(article)
            json.dump(data, file, indent=4, ensure_ascii=False)
            print(f'\n{file_name}.json was successfully created')
    else:
        print('articles not found')
else:
    print('Invalid inputs')
