from core.constant import SLACK_TOKEN
import requests, logging, json

def send(post: dict) -> None:
    try:
        res = requests.post('https://slack.com/api/chat.postMessage', 
            headers = {
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': 'Bearer ' + SLACK_TOKEN
            }, 
            data = json.dumps({
                'channel': post['channel'],
                'id': post['id'],
                'attachments': [
                    {
                        'mrkdwn_in': ['text'],
                        'color': '#019DAA',
                        'title': post['title'],
                        'text': '<%s|더 보기>' % post['link'],
                        'footer': post['footer']
                    }
                ]
            })
        )
        res_content  = json.loads(res.text)

        if not res_content['ok'] or res.status_code != 200:
            raise Exception(res_content)

        logging.info('sended message : %s', post['channel']+'-'+post['id'])
        
    except Exception as e:
        logging.error('message sending failed : %s', post['channel']+'-'+post['id'])
        raise Exception(e)
