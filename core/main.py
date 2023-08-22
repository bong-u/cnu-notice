import os, sys
isProd = True
# 테스트 환경인 경우
if len(sys.argv) > 1 and sys.argv[1] == '-test':
    sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
    # 테스트용 환경변수 설정
    from util.set_test_env import set_test_env
    isProd = False

import logging

from database import Database
from scraper import Scraper
from slack_api import send
from constant import BOARD_INFO_LIST

if __name__ == '__main__':
    if isProd:
        logging.info ('RUNNING IN PRODUCTION ENVIRONMENT')
    else:
        logging.info('RUNNING IN TEST ENVIRONMENT')
    
    # init database
    db = Database()

    # get recent post id from DB
    recent_post = db.get_data()
    # init recent post id
    new_recent_post = [0, 0, 0, 0]
    # init post list
    post_list = []

    # scrape
    for index, board in enumerate(BOARD_INFO_LIST.values()):
        new_recent_post[index], new_post_list = board['scraper'](recent_post[index], board)
        post_list += new_post_list

    logging.info("result of scraping : %s", [post['board']+'-'+post['id'] for post in post_list])

    # send to slack
    for post in post_list:
        send(post)

    # update DB
    db.update_data(new_recent_post)



