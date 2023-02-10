class Purchase:
    def __init__(self,bought,id,oldbought=0):
        self.__bought = bought
        self.__id = id
        self.__oldbought = oldbought

    def get_bought(self):
        self.__bought += self.__oldbought
        self.__oldbought = self.__bought
        return self.__bought

