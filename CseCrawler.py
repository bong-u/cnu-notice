from bs4 import BeautifulSoup
import requests

class CseCrawler:

    __URL_BASE = 'https://computer.cnu.ac.kr/computer/notice/'
    __TYPE = {
        'bachelor' : {
            'url' : __URL_BASE + 'bachelor.do',
            'name' : '학사공지'
        },
        'notice' : {
            'url' : __URL_BASE + 'notice.do',
            'name' : '일반공지'
        },
        'project' : {
            'url' : __URL_BASE + 'project.do',
            'name' : '사업단소식',
        }
    }
    __POST_LIST = []
    __RECENT_POST = []

    def __init__(self, recent_post):
        self.__RECENT_POST = recent_post

        for index, type in enumerate(['bachelor', 'notice', 'project']):
            recent_post[index], posts = self.__crawl(type)
            self.__POST_LIST += posts
    
    def __crawl(self, type):

        new_recent_post = 0

        res = requests.get (self.__TYPE[type]['url'], headers={'User-Agent':'Mozilla/5.0'})

        soup = BeautifulSoup(res.text, 'html.parser')

        for board in soup.select('div.content-wrap tbody'):
            for index, notice in enumerate(board.select('tr:not(.b-top-box)')):
                element = notice.find('a')

                href = element['href']
                title = element.text.strip()
                post_no = href.split('articleNo=')[1].split('&')[0]

                if index == 0:
                    new_recent_post = post_no
                if post_no == self.__RECENT_POST:
                    break

                self.__POST_LIST.append({
                    'title' : title,
                    'link' : self.__TYPE[type]['url'] + href,
                    'footer' : self.__TYPE[type]['name']
                })

        self.__RECENT_POST = new_recent_post
    
    def get_post_list(self):
        return self.__POST_LIST

    def get_recent_post(self):
        return self.__RECENT_POST
