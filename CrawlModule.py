from bs4 import BeautifulSoup
import requests, time

class CrawlModule():
    MAX_RETRIES = 3

    @classmethod
    def _get_soup(cls, url:str):
        for _ in range(cls.MAX_RETRIES):
            try:
                res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
                res.encoding = 'UTF-8'
                return BeautifulSoup(res.text, 'html.parser')
            except requests.exceptions.ConnectionError:
                print("ConnectionError occurred. Retrying in 1 second...")
                time.sleep(retry_delay)
        
        raise Exception("ConnectionError occurred too many times.")

    @classmethod
    def crawl_cnu(cls, recent_post:int, board_info:dict) -> tuple:
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        for item in soup.select('table > tbody > tr'):
            cells = item.findAll('td')

            # 공지는 제외
            if cells[0].text == '공지':
                continue

            post_id = int(cells[1].find('a')['href'].split('no=')[1].split('&')[0])

            # 최근 게시물 id 갱신
            if new_recent_post == 0:
                new_recent_post = post_id
            # 최근 게시물보다 오래된 게시물이면 break
            if post_id <= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : cells[1].find('a').text,
                # link = url_base + href
                'link' : cells[1].find('a')['href'].replace('.', board_info['url_base']),
                'footer' : item.select('td')[2].text
            })

        # 최근 게시물을 가장 마지막으로 보내기 위해 reverse
        return new_recent_post, list(reversed(posts))
    
    @classmethod
    def crawl_cse(cls, recent_post:int, board_info:dict) -> tuple:
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        board = soup.select_one('div.content-wrap tbody')
    
        for index, row in enumerate(board.select('tr:not(.b-top-box)')):
            element = row.find('a')

            # 공지는 제외
            post_id = int(element['href'].split('articleNo=')[1].split('&')[0])

            # 최근 게시물 id 갱신
            if index == 0:
                new_recent_post = post_id
            # 최근 게시물보다 오래된 게시물이면 break
            if post_id <= recent_post:
                break

            posts.append({
                'channel' : board_info['channel_id'],
                'title' : element.text.strip(),
                # link = url_base + href
                'link' : board_info['url'] + element['href'],
                'footer' : board_info['label']
            })

        # 최근 게시물을 가장 마지막으로 보내기 위해 reverse
        return new_recent_post, list(reversed(posts))