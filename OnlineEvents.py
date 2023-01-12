import Events

class OnlineEvents(Events.Events):

    count = 0
    def __init__(self, name, description, date):
        super().__init__(name,description,date)
        OnlineEvents.count += 1
        self.__online_event_id = OnlineEvents.count

    def get_online_event_id(self):
        return self.__online_event_id







