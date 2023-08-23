import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from core.scraper import Scraper
from util.set_test_env import set_test_env
from util.test_wrapper import test_wrapper
from core.common import BOARD_INFO_LIST

import unittest
from bs4 import BeautifulSoup

class ScraperTest(unittest.TestCase):
    
    @test_wrapper
    def test_get_soup(self):
        # given
        
        for board in BOARD_INFO_LIST.values(): 
            # when
            soup = Scraper._get_soup(board['url'])

            # then
            assert type(soup) == BeautifulSoup
    
    @test_wrapper
    def test_scrape_all_board(self):
        # given
        for board in BOARD_INFO_LIST.values():
            print ('current board : ', board['name'])
            # when
            recent_post, posts = board['scraper'](0, board)
            assert type(recent_post) == int
            post_id_list = []
            for post in posts:
                post_id_list.append(post['id'])
                assert post['id'].isnumeric()
            print ('post id list :', post_id_list)


if __name__ == '__main__':  
    unittest.main()