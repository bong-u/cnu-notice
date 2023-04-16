from bs4 import BeautifulSoup
import requests

class CrawlModule():

    @classmethod
    def _get_soup(cls, url:str):
        res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
        res.encoding = 'UTF-8'
        return BeautifulSoup(res.text, 'html.parser')

    @classmethod
    def crawl_cnu(cls, recent_post:int, board_info:dict) -> tuple:
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        for item in soup.select('table > tbody > tr'):
            cells = item.findAll('td')

            if cells[0].text == '공지':
                continue

            post_id = int(cells[1].find('a')['href'].split('no=')[1].split('&')[0])

            if new_recent_post == 0:
                new_recent_post = post_id
            if post_id <= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : cells[1].find('a').text,
                'link' : cells[1].find('a')['href'].replace('.', board_info['url_base']),
                'footer' : item.select('td')[2].text
            })

        return new_recent_post, list(reversed(posts))
    
    @classmethod
    def crawl_cse(cls, recent_post:int, board_info:dict) -> tuple:
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        board = soup.select_one('div.content-wrap tbody')
    
        for index, row in enumerate(board.select('tr:not(.b-top-box)')):
            element = row.find('a')

            post_id = int(element['href'].split('articleNo=')[1].split('&')[0])

            if index == 0:
                new_recent_post = post_id
            if post_id <= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : element.text.strip(),
                'link' : board_info['url'] + element['href'],
                'footer' : board_info['label']
            })

        return new_recent_post, list(reversed(posts))