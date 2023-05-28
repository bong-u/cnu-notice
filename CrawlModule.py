from bs4 import BeautifulSoup
import requests, time, logging

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
                logging.ERROR("ConnectionError occurred. Retrying in 3 second...")
                time.sleep(3)
        
        raise Exception("ConnectionError occurred too many times.")

    @classmethod
    def crawl_cnu(cls, recent_post:int, board_info:dict) -> tuple:
        new_recent_post = 0
        posts = []

        soup = cls._get_soup(board_info['url'])

        for item in soup.select('table > tbody > tr'):
            cells = item.findAll('td')

            # href에서 no만 추출
            post_id = int(cells[1].find('a')['href'].split('no=')[1].split('&')[0])

            # 최근 게시물 id 갱신
            new_recent_post = max(new_recent_post, post_id)

            # 새로운 게시물인 경우 posts에 추가                                                                                                                                                                                                            # 새로운 게시물인 경우 posts에 추가
            if post_id > recent_post:
                posts.append({
                    'channel' : board_info['channel_id'],
                    'title' : cells[1].find('a').text,
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
    
        for row in board.select('tr'):
            element = row.find('a')

            # href에서 articleNo만 추출
            post_id = int(element['href'].split('articleNo=')[1].split('&')[0])

            # 최근 게시물 id 갱신
            new_recent_post = max(new_recent_post, post_id)
            
            # 새로운 게시물인 경우 posts에 추가
            if post_id > recent_post:
                posts.append({
                    'channel' : board_info['channel_id'],
                    'title' : element.text.strip(),
                    'link' : board_info['url'] + element['href'],
                    'footer' : row.select('td')[3].text,
                })

        # 최근 게시물을 가장 마지막으로 보내기 위해 reverse
        return new_recent_post, list(reversed(posts))
