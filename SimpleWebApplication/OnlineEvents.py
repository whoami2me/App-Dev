import Events


class OnlineEvents(Events.Events):

    count = 0

    def __init__(self, name, image, description, date, status, date_created):
        super().__init__(name, image, description, date)
        OnlineEvents.count += 1
        self.__online_event_id = OnlineEvents.count
        self.__status = status
        self.__date_created = date_created

    def set_status(self,status):
        self.__status = status

    def get_status(self):
        return self.__status

    def get_date_created(self):
        return self.__date_created

    def get_online_event_id(self):
        return self.__online_event_id
