import Events


class OnlineEvents(Events.Events):

    count = 0

    def __init__(self, name, image, description, date, end_date, location, event_status, reg_status ,date_created):
        super().__init__(name, image, description, date, end_date,location)
        OnlineEvents.count += 1
        self.__online_event_id = OnlineEvents.count
        self.__event_status = event_status
        self.__reg_status = reg_status
        self.__date_created = date_created

    def set_event_status(self,event_status):
        self.__event_status = event_status

    def set_reg_status(self,reg_status):
        self.__reg_status = reg_status

    def get_event_status(self):
        return self.__event_status

    def get_reg_status(self):
        return self.__reg_status

    def get_date_created(self):
        return self.__date_created

    def get_online_event_id(self):
        return self.__online_event_id
