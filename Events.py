class Events:

    count_id = 0

    def __init__(self,name,description, date):

        Events.count_id += 1
        self.__event_id = Events.count_id
        self.__name = name
        self.__description = description
        self.__expiry_date = date

    def set_name(self, name):
        self.__name = name

    def set_description(self,  description):
        self.__description = description

    def set_date(self, date):
        self.__expiry_date = date

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_date(self):
        return self.__date

    def get_event_id(self):
        return self.__event_id

