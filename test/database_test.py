import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from core.database import Database
from core.common import BOARD_TYPE
from util.set_test_env import set_test_env
from util.test_wrapper import test_wrapper

import unittest, logging
from unittest.mock import patch

class DatabaseTest(unittest.TestCase):

    @test_wrapper
    @unittest.skip(reason='skip')
    def test_get_data(self):
        # given # when
        db = Database()

        for board_type in BOARD_TYPE:
            # when
            data = db.get_data(board_type)
            # then
            assert type(data) == int
    
    @test_wrapper
    @patch('core.database.redis.Redis.get', return_value=None)
    def test_get_data_non_exist_key (self, mock_redis_get):
        # given
        db = Database()
        # when # then
        with self.assertRaises(KeyError) as context:
            db.get_data(BOARD_TYPE.CNU_NOTICE)
        
        logging.info('exception : ' + str(context.exception))
        mock_redis_get.assert_called_once_with(BOARD_TYPE.CNU_NOTICE.value)
    
    
    @test_wrapper
    @patch('core.database.redis.Redis.get', return_value='abc')
    def test_get_data_non_nummeric_value(self, mock_redis_get):
        # given
        db = Database()
        # when # then
        with self.assertRaises(TypeError) as context:
            db.get_data(BOARD_TYPE.CNU_NOTICE)
        
        logging.info('exception : ' + str(context.exception))
        mock_redis_get.assert_called_once_with(BOARD_TYPE.CNU_NOTICE.value)
    
    @test_wrapper
    @unittest.skip(reason='skip')
    def test_update_data(self):
        # given
        db = Database()

        for board_type in BOARD_TYPE:
            data = db.get_data(board_type)
            # update original data as it is
            # when # then
            assert db.update_data(board_type, data) == data

if __name__ == '__main__':  
    unittest.main()