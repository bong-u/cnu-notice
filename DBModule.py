import gspread, logging

class DBModule:
    def __init__(self):
        self.__CELLS = ['A2', 'B2', 'C2', 'D2']
        self.gc = gspread.service_account(filename='gspread_auth.json')
        self.sh = self.gc.open("cse_notice").sheet1

        # get A2, B2, C2, D2 
        self.__data = [int(self.sh.get(cell)[0][0]) for cell in self.__CELLS]

    def get_data(self) -> list:
        return self.__data

    def update_data(self, new_data):
        log = []

        for i in range(len(self.__CELLS)):
            # 기존 값과 다르면 update
            if self.__data[i] != new_data[i]:
                log += ['%s : %d -> %d' % (self.__CELLS[i], self.__data[i], new_data[i])]
                self.sh.update_acell(self.__CELLS[i], new_data[i])

        logging.info("DB updated : %s", log)