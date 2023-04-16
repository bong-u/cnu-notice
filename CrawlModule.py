from bs4 import BeautifulSoup
import requests

class CrawlModule():

    @classmethod
    def _get_soup(cls, url):
        res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
        res.encoding = 'UTF-8'
        return BeautifulSoup(res.text, 'html.parser')

    @classmethod
    def crawl_cnu(cls, recent_post, board_info):
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        for item in soup.select('table > tbody > tr'):
            cells = []
            for column in item.select('td'):
                cells.append(column.text)

            if cells[0] == '공지':
                continue
            if new_recent_post == 0:
                new_recent_post = cells[0]
            if cells[0] == recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : cells[1],
                'link' : item.select_one('a')['href'].replace('.', board_info['url_base']),
                'footer' : cells[2]
            })

        return new_recent_post, reversed(posts)
    
    @classmethod
    def crawl_cse(cls, recent_post, board_info):
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        board = soup.select_one('div.content-wrap tbody')
        for index, notice in enumerate(board.select('tr:not(.b-top-box)')):
            element = notice.find('a')

            href = element['href']
            title = element.text.strip()
            post_id = href.split('articleNo=')[1].split('&')[0]

            if index == 0:
                new_recent_post = post_id
            if post_id >= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : title,
                'link' : board_info['url'] + href,
                'footer' : board_info['label']
            })

        return new_recent_post, reversed(posts)