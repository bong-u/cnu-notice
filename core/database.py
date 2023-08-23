import os, redis, logging
from core.common import BOARD_TYPE

class Database:
    def __init__(self) -> None:
        self.__r = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True)

    def get_data(self, board_type: BOARD_TYPE) -> int:
        data = self.__r.get(board_type.value)
        if data == None:
            raise KeyError('No key(%s) in db' % board_type.value)
        if not data.isnumeric():
            raise TypeError('Value of key(%s) is not numeric' % board_type.value)

        logging.info('db get : %s : %s' % (board_type.value, data))        
        return int(data)

    def update_data(self, board_type: BOARD_TYPE, data: int) -> int:
        self.__r.set(board_type.value, data)
        logging.info('db update : %s : %s' % (board_type.value, data))
        return data 