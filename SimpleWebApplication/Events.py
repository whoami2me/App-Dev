class Events:

    count_id = 0

    def __init__(self, name, image ,description, date, location):
        Events.count_id += 1
        self.__event_id = Events.count_id
        self.__image = image
        self.__name = name
        self.__description = description
        self.__date = date
        self.__location = location


    def set_image(self, image):
        self.__image = image

    def set_name(self, name):
        self.__name = name

    def set_description(self,  description):
        self.__description = description

    def set_date(self, date):
        self.__date = date

    def set_location(self, location):
        self.__location = location

    def get_image(self):
        return self.__image

    def get_name(self):
        return self.__name

    def get_description(self):
        return self.__description

    def get_date(self):
        return self.__date

    def get_location(self):
        return self.__location

    def get_event_id(self):
        return self.__event_id




