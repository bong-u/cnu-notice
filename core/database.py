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
        data = int(self.__r.get(board_type.value))
        logging.info('db get : %s : %d' % (board_type.value, data))        
        return data

    def update_data(self, board_type: BOARD_TYPE, data: int) -> int:
        self.__r.set(board_type.value, data)
        logging.info('db update : %s : %d' % (board_type.value, data))
        return data 