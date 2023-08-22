import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from util.set_test_env import set_test_env
from util.test_wrapper import test_wrapper
from core.slack_api import send

import unittest, logging

class SlackApiTest(unittest.TestCase):

    @test_wrapper
    def test_send(self):
        # given
        test_post = {
            'title': 'test_title',
            'channel': os.environ['CHANNEL_CNU'],
            'id': '12345',
            'link': 'https://www.google.com',
            'footer': 'test_author',
        }

        # when # then
        assert send(test_post) == None

if __name__ == '__main__':  
    unittest.main()