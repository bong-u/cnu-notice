from bs4 import BeautifulSoup
import requests

class CnuCrawler:

    __URL_BASE = 'https://plus.cnu.ac.kr/_prog/_board'
    __URL = __URL_BASE + '/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702'

    __POST_LIST = []
    __RECENT_POST = 0

    def __init__(self, recent_post):
        self.__RECENT_POST = recent_post
        self.__crawl()
    
    def __crawl(self):
        new_recent_post = 0

        res = requests.get (self.__URL, headers={'User-Agent':'Mozilla/5.0'})
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
            if L[0] == self.__RECENT_POST:
                break

            self.__POST_LIST.append({
                'title' : L[1],
                'link' : item.select_one('a')['href'].replace('.', self.__URL_BASE),
                'footer' : L[2]
            })

        self.__RECENT_POST = new_recent_post
    
    def get_post_list(self):
        return self.__POST_LIST

    def get_recent_post(self):
        return [self.__RECENT_POST]