import Events

class OnlineEvents(Events.Events):

    count = 0
    def __init__(self, name, description, date, image):
        super().__init__(name,description,date)
        OnlineEvents.count += 1
        self.__online_event_id = OnlineEvents.count
        self.__image = image

    def set_image(self, image):
        self.__image = image

    def get_image(self):
        return self.__image

    def get_online_event_id(self):
        return self.__online_event_id







