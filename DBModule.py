import gspread

class DBModule:

    __gc = gspread.service_account(filename='gspread_auth.json')
    __sh = __gc.open("cse_notice").sheet1
    
    def read(self):
        data = [0, 0, 0, 0]
        data[0] = self.__sh.get('A2')[0][0]
        data[1] = self.__sh.get('B2')[0][0]
        data[2] = self.__sh.get('C2')[0][0]
        data[3] = self.__sh.get('D2')[0][0]

        return data
    
    def update(self, new_data):
        self.__sh.update_acell('A2', new_data[0])
        self.__sh.update_acell('B2', new_data[1])
        self.__sh.update_acell('C2', new_data[2])
        self.__sh.update_acell('D2', new_data[3])

if __name__ == '__main__':
    pass