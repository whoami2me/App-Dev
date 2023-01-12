import Events

class OfflineEvents(Events.Events):

    count = 0
    def __init__(self, name, description, date, pax, location):
        super().__init__(name,description,date)
        self.__pax = pax
        self.__location = location

    def set_pax(self, pax):
        self.__pax = pax

    def get_pax(self):
        return self.__pax

    def set_location(self, location):
        self.__location = location

    def get_location(self):
        return self.__location

