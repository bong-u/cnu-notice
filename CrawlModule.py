from bs4 import BeautifulSoup
import requests

class CrawlModule():

    @staticmethod
    def CrawlCNU(recent_post, board_info):
        new_recent_post = 0
        post_list = []

        res = requests.get (board_info['url'], headers={'User-Agent':'Mozilla/5.0'})
        res.encoding = 'UTF-8'
        soup = BeautifulSoup(res.text, 'html.parser')

        for item in soup.select('table > tbody > tr'):
            L = []
            for column in item.select('td'):
                L.append(column.text)

            if L[0] == '공지':
                continue
            if new_recent_post == 0:
                new_recent_post = L[0]
            if L[0] == recent_post:
                break

            post_list.append({
                'channel' : board_info['channel_id'],
                'title' : L[1],
                'link' : item.select_one('a')['href'].replace('.', board_info['url_base']),
                'footer' : L[2]
            })

        return new_recent_post, reversed(post_list)
    
    @staticmethod
    def CrawlCSE(recent_post, board_info):
        new_recent_post = 0
        post_list = []

        res = requests.get (board_info['url'], headers={'User-Agent':'Mozilla/5.0'})

        soup = BeautifulSoup(res.text, 'html.parser')

        board = soup.select_one('div.content-wrap tbody')
        for index, notice in enumerate(board.select('tr:not(.b-top-box)')):
            element = notice.find('a')

            href = element['href']
            title = element.text.strip()
            post_no = href.split('articleNo=')[1].split('&')[0]

            if index == 0:
                new_recent_post = post_no
            if post_no == recent_post:
                break

            post_list.append({
                'channel' : board_info['channel_id'],
                'title' : title,
                'link' : board_info['url'] + href,
                'footer' : board_info['label']
            })

        return new_recent_post, reversed(post_list)