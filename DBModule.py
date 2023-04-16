import gspread

class DBModule:
    def __init__(self):
        self.gc = gspread.service_account(filename='gspread_auth.json')
        self.sh = self.gc.open("cse_notice").sheet1
        self.__data = [int(self.sh.get('A2')[0][0]), int(self.sh.get('B2')[0][0]), int(self.sh.get('C2')[0][0]), int(self.sh.get('D2')[0][0])]

    def get_data(self) -> list:
        return self.__data

    def update_data(self, new_data):
        # member 변수 update
        self.__data = new_data
        # google sheet update
        self.sh.update_acell('A2', new_data[0])
        self.sh.update_acell('B2', new_data[1])
        self.sh.update_acell('C2', new_data[2])
        self.sh.update_acell('D2', new_data[3])