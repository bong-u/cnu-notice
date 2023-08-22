import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from core.database import Database
from util.set_test_env import set_test_env
from util.test_wrapper import test_wrapper

import unittest, logging

class DatabaseTest(unittest.TestCase):

    @test_wrapper
    def test_get_data(self):
        # given # when
        data = Database().get_data()

        # then
        logging.info ('db data : '+ str(data))
        assert type(data) == list
        assert len(data) == 4
        for i in range(len(data)):
            assert type(data[i]) == int
    
    @test_wrapper
    def test_set_data(self):
        # given
        db = Database()
        origin_data = Database().get_data()
        
        # when
        logging.info ('update data for test')
        new_data = [i+1 for i in range(len(origin_data))]
        Database().update_data(new_data)

        # then
        data = Database().get_data()

        assert type(data) == list
        assert len(data) == 4
        for i in range(len(data)):
            assert data[i] == new_data[i]
        
        logging.info ('revert to origin data')
        Database().update_data(origin_data)

if __name__ == '__main__':  
    unittest.main()