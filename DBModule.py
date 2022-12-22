import os, gspread

class DBModule:

    __gc = gspread.service_account(filename='cse-notice-api-c962bfa795cd.json')
    __sh = __gc.open("cse_notice").sheet1
    __data = [0, 0, 0]
    
    def read(self):
        data = [0, 0, 0]
        data[0] = self.__sh.get('A2')[0][0]
        data[1] = self.__sh.get('B2')[0][0]
        data[2] = self.__sh.get('C2')[0][0]

        return data
    
    def update(self, new_data):
        self.__sh.update_acell('A2', new_data[0])
        self.__sh.update_acell('B2', new_data[1])
        self.__sh.update_acell('C2', new_data[2])

if __name__ == '__main__':
    pass