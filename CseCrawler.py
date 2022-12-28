from bs4 import BeautifulSoup
import requests

class CseCrawler:

    __URL_BASE = 'https://computer.cnu.ac.kr/computer/notice/'
    __TYPES = [
        {
            'idx' : 0,
            'name' : 'bachelor',
            'url' : __URL_BASE + 'bachelor.do',
            'label' : '학사공지'
        },
        {
            'idx' : 1,
            'name' : 'notice',
            'url' : __URL_BASE + 'notice.do',
            'label' : '일반공지'
        },
        {
            'idx' : 2,
            'name': 'project',
            'url' : __URL_BASE + 'project.do',
            'label' : '사업단소식',
        }
    ]
    __POST_LIST = []
    __RECENT_POST = []

    def __init__(self, recent_post):
        self.__RECENT_POST = recent_post

        for type in self.__TYPES:
            self.__crawl(type)
    
    def __crawl(self, type):
        new_recent_post = 0

        res = requests.get (type['url'], headers={'User-Agent':'Mozilla/5.0'})

        soup = BeautifulSoup(res.text, 'html.parser')

        board = soup.select_one('div.content-wrap tbody')
        for index, notice in enumerate(board.select('tr:not(.b-top-box)')):
            element = notice.find('a')

            href = element['href']
            title = element.text.strip()
            post_no = href.split('articleNo=')[1].split('&')[0]

            if index == 0:
                new_recent_post = post_no
            if post_no == self.__RECENT_POST[type['idx']]:
                break

            self.__POST_LIST.append({
                'title' : title,
                'link' : type['url'] + href,
                'footer' : type['label']
            })

        self.__RECENT_POST[type['idx']] = new_recent_post
    
    def get_post_list(self):
        return self.__POST_LIST

    def get_recent_post(self):
        return self.__RECENT_POST
