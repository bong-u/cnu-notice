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
            cells = item.findAll('td')

            element = cells[1].find('a')
            href = element['href']
            post_id = href.split('no=')[1].split('&')[0]
            label = item.select('td')[2].text

            if cells[0].text == '공지':
                continue
            if new_recent_post == 0:
                new_recent_post = post_id
            if post_id <= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : element.text,
                'link' : href.replace('.', board_info['url_base']),
                'footer' : label
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
            if post_id <= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : title,
                'link' : board_info['url'] + href,
                'footer' : board_info['label']
            })

        return new_recent_post, reversed(posts)