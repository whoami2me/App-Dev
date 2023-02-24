import Events


class OfflineEvents(Events.Events):

    count = 0

    def __init__(self, name, image, description, date, end_date, location, pax, latitude, longitude, event_status, reg_status, date_created):
        super().__init__(name, image, description, date, end_date, location)
        OfflineEvents.count += 1
        self.__offline_event_id = OfflineEvents.count
        self.__pax = pax
        self.__latitude = latitude
        self.__longitude = longitude
        self.__event_status = event_status
        self.__reg_status = reg_status
        self.__date_created = date_created
        self.__registered_pax = None

    def set_pax(self, pax):
        self.__pax = pax

    def set_latitude(self, latitude):
        self.__latitude = latitude

    def set_longitude(self, longitude):
        self.__longitude = longitude

    def set_event_status(self,event_status):
        self.__event_status = event_status

    def set_reg_status(self,reg_status):
        self.__reg_status = reg_status

    def set_reg_pax(self, reg_pax):
        self.__registered_pax = reg_pax

    def get_pax(self):
        return self.__pax

    def get_latitude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude

    def get_event_status(self):
        return self.__event_status

    def get_reg_status(self):
        return self.__reg_status

    def get_date_created(self):
        return self.__date_created

    def get_offline_event_id(self):
        return self.__offline_event_id

    def get_reg_pax(self):
        return self.__registered_pax
