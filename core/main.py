import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
isProd = True
# 테스트 환경인 경우
if len(sys.argv) > 1 and sys.argv[1] == '-test':
    # 테스트용 환경변수 설정
    from util.set_test_env import set_test_env
    isProd = False

import logging, core

from database import Database
from scraper import Scraper
from slack_api import send
from common import BOARD_INFO_LIST, BOARD_TYPE

if __name__ == '__main__':
    if isProd:
        logging.info ('RUNNING IN PRODUCTION ENVIRONMENT')
    else:
        logging.info('RUNNING IN TEST ENVIRONMENT')
    
    # init database
    db = Database()

    # get recent post id from DB
    recent_post = {}
    new_recent_post = {}
    for board_type in BOARD_TYPE:
        new_recent_post[board_type.value] = 0
        recent_post[board_type.value] = db.get_data(board_type)
    
    # init post list
    post_list = []

    # scrape
    for board_type in [element.value for element in BOARD_TYPE]:
        board_info = BOARD_INFO_LIST[board_type]
        new_recent_post[board_type], new_post_list = board_info['scraper'](recent_post[board_type], board_info)\
        
        if new_post_list:
            logging.info('new post: %s', [post['board']+'-'+post['id'] for post in new_post_list])
        post_list += new_post_list


    # send to slack
    for post in post_list:
        send(post)

    # update DB
    for board_type in BOARD_TYPE:
        if recent_post[board_type.value] != new_recent_post[board_type.value]:
            db.update_data(board_type, new_recent_post[board_type.value])
