import requests
from bs4 import BeautifulSoup

# url = 'https://search.naver.com/search.naver?where=news&ie=utf8&sm=nws_hty&query=ESG'

def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        ul = soup.select_one('ul.list_news')
        links = ul.select('li > div > div > div.news_contents > a.dsc_thumb')
        titles = ul.select('li > div > div > div.news_contents > a.news_tit')
        t = [title.get_text() for title in titles]
        l = [link.get('href') for link in links]
        data = {'title': t, 'link': l}
        print(data)
        return data
    else:
        return response.status_code



