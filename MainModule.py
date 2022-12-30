import requests
import os, json
from datetime import datetime
from DBModule import DBModule
from CrawlModule import CrawlModule

class MainModule(DBModule):
    __SLACK_TOKEN = os.getenv('SLAC K_TOKEN')
    __CHANNEL_ID = os.getenv('CHANNEL_ID')
    __CSE_URL_BASE = 'https://computer.cnu.ac.kr/computer/notice/'
    __CNU_URL_BASE = 'https://plus.cnu.ac.kr/_prog/_board'

    __BOARD_INFO_LIST = [
        {
            'url' : __CSE_URL_BASE + 'bachelor.do',
            'label' : '학사공지'
        },
        {
            'url' : __CSE_URL_BASE + 'notice.do',
            'label' : '일반공지'
        },
        {
            'url' : __CSE_URL_BASE + 'project.do',
            'label' : '사업단소식'
        },
        {
            'url_base' : __CNU_URL_BASE,
            'url' : __CNU_URL_BASE + '/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702'
        }
    ]

    def __init__(self):
        super(MainModule, self).__init__()

        print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | project running...')

        recent_post = self.getFromDB()

        post_list = []

        recent_post[0], new_post = CrawlModule.CrawlCSE(recent_post[0], self.__BOARD_INFO_LIST[0])
        post_list += new_post
        recent_post[1], new_post = CrawlModule.CrawlCSE(recent_post[1], self.__BOARD_INFO_LIST[1])
        post_list += new_post
        recent_post[2], new_post = CrawlModule.CrawlCSE(recent_post[2], self.__BOARD_INFO_LIST[2])
        post_list += new_post
        recent_post[3], new_post = CrawlModule.CrawlCNU(recent_post[3], self.__BOARD_INFO_LIST[3])
        post_list += new_post

        # seriallize post_list
        message_list = self.serialize(post_list)

        # self.update(recent_post)

        # for message in message_list:
        #     self.send(message)

    def serialize(self, post_list):
        message_list= []
        
        for item in post_list:
            print (item)
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