from typing import List, Dict

from bs4 import BeautifulSoup as Soup
from datetime import datetime
import requests
import json


def get_inputs() -> Dict[str, str]:
    limit = input(
        'Enter how many articles to format or leave blank(15): ') or '15'
    to_date = input(
        'Enter to date or leave blank(2022-07-04): YYYY-MM-DD ') or '2022-07-04'
    from_date = input(
        'Enter from date or leave blank(2007:57:33): YYYY:MM:DD ') or '2007:57:33'
    file_name = input(
        'Enter new file name or leave blank($date_news.json): ') or f'{datetime.now().date()}_news'
    return {'limit': limit,
            'to_date': to_date,
            'from_date': from_date,
            'file_name': file_name}


def get_response(limit: str, to_date: str, from_date: str) -> requests:
    url = f"http://newsline.kg/getNews.php?limit={limit}&last_dt={to_date}%{from_date}.933739"
    return requests.get(url)


def get_dict(response: requests) -> Dict[str, Dict[str, str]]:
    return json.loads(response.text)


def validate_news(news: Dict[str, Dict[str, str]]) -> bool:
    if news:
        if news['data']:
            return True
    raise FileNotFoundError('Invalid inputs')


def get_validated_data(news: Dict[str, Dict[str, str]]
                       ) -> List[Dict[str, Dict[str, str]]]:
    validate_news(news)
    data = []
    for art in news['data']:
        article = {
            'id': art.get('id'),
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
    return data


def write_json(data: List[Dict[str, Dict[str, str]]],
               file_name: str) -> None:
    with open(f'{file_name}.json', 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    inputs = get_inputs()
    response = get_response(
        inputs['limit'],
        inputs['to_date'],
        inputs['from_date']
    )
    news = get_dict(response)
    data = get_validated_data(news)
    write_json(data, inputs['file_name'])


if __name__ == "__main__":
    main()
