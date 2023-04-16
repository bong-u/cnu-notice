import requests
import os, json
from datetime import datetime
from DBModule import DBModule
from CrawlModule import CrawlModule

class MainModule(DBModule):
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    CNU_CHANNEL_ID = os.getenv('CNU_CHANNEL_ID')
    CSE_CHANNEL_ID = os.getenv('CSE_CHANNEL_ID')
    CSE_URL_BASE = 'https://computer.cnu.ac.kr/computer/notice/'
    CNU_URL_BASE = 'https://plus.cnu.ac.kr/_prog/_board'

    BOARD_INFO_LIST = [
        {
            'channel_id' : CSE_CHANNEL_ID,
            'url' : CSE_URL_BASE + 'bachelor.do',
            'label' : '학사공지'
        },
        {
            'channel_id' : CSE_CHANNEL_ID,
            'url' : CSE_URL_BASE + 'notice.do',
            'label' : '일반공지'
        },
        {
            'channel_id' : CSE_CHANNEL_ID,
            'url' : CSE_URL_BASE + 'project.do',
            'label' : '사업단소식'
        },
        {
            'channel_id' : CNU_CHANNEL_ID,
            'url_base' : CNU_URL_BASE,
            'url' : CNU_URL_BASE + '/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702'
        }
    ]

    def __init__(self):
        # init DB
        super(MainModule, self).__init__()

        print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | project running...')

        # get recent post id from DB
        recent_post = self.getFromDB()

        post_list = []

        # crawl
        recent_post[0], new_post = CrawlModule.crawl_cse(recent_post[0], self.BOARD_INFO_LIST[0])
        post_list += new_post
        recent_post[1], new_post = CrawlModule.crawl_cse(recent_post[1], self.BOARD_INFO_LIST[1])
        post_list += new_post
        recent_post[2], new_post = CrawlModule.crawl_cse(recent_post[2], self.BOARD_INFO_LIST[2])
        post_list += new_post
        recent_post[3], new_post = CrawlModule.crawl_cnu(recent_post[3], self.BOARD_INFO_LIST[3])
        post_list += new_post

        # serialize
        message_list = self.serialize(post_list)

        # update DB
        self.updateDB(recent_post)

        # send message
        for message in message_list:
            self.send(message)

    def serialize(self, post_list):
        message_list= []
        
        for item in post_list:
            print (item)
            message_list.append(
                {
                    'channel': item['channel'],
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
                'Authorization': 'Bearer ' + self.SLACK_TOKEN
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