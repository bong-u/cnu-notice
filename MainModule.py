import requests
import os, json, logging
from datetime import datetime
from DBModule import DBModule
from CrawlModule import CrawlModule

class MainModule(DBModule):
    SLACK_TOKEN = os.getenv('SLACK_TOKEN')
    CSE_URL_BASE = 'https://computer.cnu.ac.kr/computer/notice/'
    CNU_URL_BASE = 'https://plus.cnu.ac.kr/_prog/_board'

    BOARD_INFO_LIST = [
        {
            'name' : '컴융-학사공지',
            'channel_id' : os.getenv('CHANNEL_BACHELOR'),
            'url' : CSE_URL_BASE + 'bachelor.do',
        },
        {
            'name' : '컴융-일반소식',
            'channel_id' : os.getenv('CHANNEL_NOTICE'),
            'url' : CSE_URL_BASE + 'notice.do',
        },
        {
            'name' : '컴융-사업단소식',
            'channel_id' : os.getenv('CHANNEL_PROJECT'),
            'url' : CSE_URL_BASE + 'project.do',
        },
        {
            'name' : '충남대-학사정보',
            'channel_id' : os.getenv('CHANNEL_CNU'),
            'url_base' : CNU_URL_BASE,
            'url' : CNU_URL_BASE + '/?code=sub07_0702&site_dvs_cd=kr&menu_dvs_cd=0702'
        }
    ]

    def __init__(self):
        # init DB
        super(MainModule, self).__init__()

        # init logging
        logging.basicConfig(
            format="%(asctime)s %(levelname)-7s %(message)s",
            level=logging.INFO,
        )

        logging.info("Application started")

        # get recent post id from DB
        recent_post = self.get_data()
        new_recent_post = [0, 0, 0, 0]

        post_list = []

        # crawl
        new_recent_post[0], new_post = CrawlModule.crawl_cse(recent_post[0], self.BOARD_INFO_LIST[0])
        post_list += new_post
        new_recent_post[1], new_post = CrawlModule.crawl_cse(recent_post[1], self.BOARD_INFO_LIST[1])
        post_list += new_post
        new_recent_post[2], new_post = CrawlModule.crawl_cse(recent_post[2], self.BOARD_INFO_LIST[2])
        post_list += new_post
        new_recent_post[3], new_post = CrawlModule.crawl_cnu(recent_post[3], self.BOARD_INFO_LIST[3])
        post_list += new_post

        logging.info("Crawling result : %s", [post['board']+'-'+post['id'] for post in post_list])

        # serialize
        message_list = self.serialize(post_list)
        
        # send message
        for message in message_list:
            self.send(message)

        # update DB
        self.update_data(new_recent_post)


    def serialize(self, post_list):
        message_list= []
        
        for item in post_list:
            message_list.append(
                {
                    'channel': item['channel'],
                    'id': item['id'],
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
        try:
            res = requests.post('https://slack.com/api/chat.postMessag', 
                headers = {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Authorization': 'Bearer ' + self.SLACK_TOKEN
                }, 
                data = json.dumps(message)
            )
            res = json.loads(res.text)

            if not res['ok'] or res.status_code != 200:
                raise Exception(res)

            logging.info('Message sended : %s', message['channel']+'-'+message['id'])
            
        except Exception as e:
            logging.error('Message sending failed : %s', message['channel']+'-'+message['id'])
            logging.error('Error message : '+ str(e))
            raise Exception(e)


if __name__ == '__main__':
    MainModule()