import Events


class OfflineEvents(Events.Events):

    count = 0

    def __init__(self, name, image, description, date, pax, location, latitude, longitude, status, date_created):
        super().__init__(name, image, description, date)
        OfflineEvents.count += 1
        self.__offline_event_id = OfflineEvents.count
        self.__pax = pax
        self.__location = location
        self.__latitude = latitude
        self.__longitude = longitude
        self.__status = status
        self.__date_created = date_created

    def set_pax(self, pax):
        self.__pax = pax

    def set_location(self, location):
        self.__location = location

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def set_longitude(self, longitude):
        self.__longitude = longitude

    def set_status(self,status):
        self.__status = status

    def get_pax(self):
        return self.__pax

    def get_location(self):
        return self.__location

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude

    def get_status(self):
        return self.__status

    def get_date_created(self):
        return self.__date_created

    def get_offline_event_id(self):
        return self.__offline_event_id
