import requests
from bs4 import BeautifulSoup
import os, json
from datetime import datetime
from DBModule import DBModule

class MainModule(DBModule):
    __SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    __CHANNEL_ID = os.getenv('CHANNEL_ID')
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

    def __init__(self):
        super()

        recent_post = self.read()

        print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | project running...')

        post_list = []

        for index, type in enumerate(['bachelor', 'notice', 'project']):
            recent_post[index], posts = self.crawl(type, recent_post[index])
            post_list += posts
            # break

        message_list = self.serialize(post_list)

        self.update(recent_post)

        # self.send(message_list[0])

    def crawl(self, type, recent_post):

        post_list = []
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
                if post_no == recent_post:
                    break

                post_list.append({
                    'title' : title,
                    'link' : self.__TYPE[type]['url'] + href,
                    'footer' : self.__TYPE[type]['name']
                })
    
        return new_recent_post, post_list

    def serialize(self, post_list):
        message_list= []
        
        for item in post_list:
            message_list.append(
                {
                    'channel': self.__CHANNEL_ID,
                    'attachments': [
                        {
                            'mrkdwn_in': ['text'],
                            'color': '#019DAA',
                            'title': item['title'],
                            'text': '<%s|더 보기>' % item['link'],
                            'footer': item['footer']
                        }
                    ]
                }
            )
            
        
        return message_list

    def send(self, message):

        res = requests.post('https://slack.com/api/chat.postMessage', 
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': 'Bearer ' + self.__SLACK_TOKEN
            }, 
            data = json.dumps(message)
        )

        status = json.loads(res.text)['ok']

        if status:
            print ('Message sending success - ', message['attachments'][0]['title'])
        else:
            print ('Failed to send message.')
            print (json.loads(res.text))

if __name__ == '__main__':
    MainModule()