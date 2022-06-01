import requests
from bs4 import BeautifulSoup
import json

class Crawler:
    __record = []
    __FILE_PATH = 'record.txt'
    __SLACK_TOKEN = ''
    __URL_BASE = 'https://computer.cnu.ac.kr'

    def __init__(self):
        self.__readFile()
    
    def __readFile(self):
        
        # load record
        with open(self.__FILE_PATH, 'r') as f:
            self.__record = f.read().split(' ')
        
        # load slack token
        with open('token.json', 'r') as f:
            self.__SLACK_TOKEN = json.load(f)['token']
    
    def __writeFile(self, new_record):

        with open(self.__FILE_PATH, 'w') as f:
            f.write(new_record[0] + ' ' + new_record[1])
    
    def crawl(self):

        data = []
        new_record = ['','']
        TYPE = ['학사공지', '일반소식']
        res = requests.get (self.__URL_BASE)

        soup = BeautifulSoup(res.text, 'html.parser')

        for i, board in enumerate(soup.select('div.main-mini-box')[:2]):
            for j, notice in enumerate(board.select('li')):
                href = notice.select_one('a')['href']
                articleNo = notice.select_one('a')['href'].split('articleNo=')[1]
                text = notice.select_one('span').text.strip()

                if j == 0:
                    new_record[i] = articleNo
                if articleNo == self.__record[i]:
                    break

                data.append({
                    'type' : TYPE[i],
                    'href' : href,
                    'text' : text
                })

        self.__writeFile(new_record)
        return data
    
    def serialize(self, data):
        messages = []
        
        for item in data:
            msg = {
                'channel': 'C03HU2GJRAQ',
                'attachments': [
                    {
                        'mrkdwn_in': ['text'],
                        'color': '#019DAA',
                        'title': item['text'],
                        'text': '<{}|더보기>'.format(self.__URL_BASE + item['href']),
                        'footer': '충남대학교 컴퓨터융합학부 ' + item['type'],
                        'footer_icon': 'https://play-lh.googleusercontent.com/MRgAxDb-1HaJcTm1Ew0dj8_9qXOArbYfmceQG0wjkTEzJZI3snLOqAXMNjoU5ckN6ds4=w240-h480-rw'
                    }
                ]
            }
            messages.append (msg)
            
        
        return messages
        
    def send(self, message):

        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'Authorization': 'Bearer ' + self.__SLACK_TOKEN
        }

        res = requests.post('https://slack.com/api/chat.postMessage', 
            headers = headers, 
            data = json.dumps(message)
        )

        status = json.loads(res.text)['ok']

        if status:
            print ('Message sending success.')
        else:
            print ('Failed to send message.')
            print (json.loads(res.text))
    
if __name__ == '__main__':
    crawler = Crawler()
    data = crawler.crawl()
    messages = crawler.serialize(data)
    
    for msg in messages:
        crawler.send(msg)
