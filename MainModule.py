import requests
from bs4 import BeautifulSoup
import os, json
from datetime import datetime
from DBModule import DBModule
from CseCrawler import CseCrawler

class MainModule(DBModule):
    __SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    __CHANNEL_ID = os.getenv('CHANNEL_ID')

    def __init__(self):
        super()

        recent_post = self.read()

        print (datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' | project running...')

        post_list = []

        cse_crawler = CseCrawler(recent_post)
        post_list = cse_crawler.get_post_list()

        message_list = self.serialize(post_list)

        self.update(recent_post)

        for message in message_list:
            self.send(message)

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