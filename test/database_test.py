import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from core.database import Database
from core.common import BOARD_TYPE
from util.set_test_env import set_test_env
from util.test_wrapper import test_wrapper

import unittest, logging

class DatabaseTest(unittest.TestCase):

    @test_wrapper
    def test_get_data(self):
        # given # when
        db = Database()

        for board_type in BOARD_TYPE:
            # when
            data = db.get_data(board_type)
            # then
            assert type(data) == int
    
    @test_wrapper
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