import requests as rq
import bs4
import wget
import os


def parse_page(text):
    soup = bs4.BeautifulSoup(text, 'html.parser')
    arr = [link.get('href') for link in soup.find_all('a', 'uk-link-toggle')]
    return arr


def get_web_page(url):
    r = rq.get(url)
    text_page = r.text
    return text_page


if __name__ == '__main__':
    text = get_web_page("https://www.mirea.ru/schedule/")
    array_of_urls = parse_page(text)[:49]
    os.makedirs('files/')
    for url in array_of_urls:
        wget.download(url, out="files/")
