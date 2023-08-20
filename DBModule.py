import os, redis, logging

class DBModule:
    def __init__(self) -> None:
        self.__r = redis.Redis(
            host=os.getenv('REDIS_HOST'),
            port=int(os.getenv('REDIS_PORT')),
            password=os.getenv('REDIS_PASSWORD'),
            decode_responses=True)
        
        self.__KEYS = ['cse-bachelor', 'cse-notice', 'cse-project', 'cnu-notice']

        self.__data = [int(self.__r.get(key)) for key in self.__KEYS]

    def get_data(self) -> list:
        return self.__data

    def update_data(self, new_data: list) -> None:
        log = []

        for index in range(len(self.__KEYS)):
            # 기존 값과 다르면 update
            if self.__data[index] != new_data[index]:
                log += ['%s : %d -> %d' % (self.__KEYS[index], self.__data[index], new_data[index])]
                self.__r.set(self.__KEYS[index], new_data[index])

        logging.info("DB updated : %s", log)