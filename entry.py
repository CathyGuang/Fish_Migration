# The entry object
class Entry:
    def __init__(self, fishNum, temp):
        self.fishNum = fishNum
        self.temp = temp
    
    def __repr__(self):
        # out = '{' + str(self.fishNum) + '; ' + str(self.temp) + '}'
        # out = str(self.temp)
        out = str(self.fishNum)
        return out

    def get_fishNum(self):
        return self.fishNum
    
    def get_temp(self):
        return self.temp
    
    def moveIn(self, number):
        self.fishNum += number

    def moveOut(self, number):
        self.fishNum -= number
    