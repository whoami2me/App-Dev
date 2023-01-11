class Events:

    count_id = 0

    def __init__(self,name,types,description,vacancies,expiry_date):

        Events.count_id += 1
        self.__event_id = Events.count_id
        self.__name = name
        self.__types = types
        self.__description = description
        self.__vacancies = vacancies
        self.__expiry_date = expiry_date

    def set_name(self, name):
        self.__name = name

    def set_types(self, types):
        self.__types = types

    def set_description(self,  description):
        self.__description = description

    def set_vacancies(self, vacancies):
        self.__vacancies = vacancies

    def set_expiry_date(self, expiry_date):
        self.__expiry_date = expiry_date

    def get_name(self):
        return self.__name

    def get_types(self):
        return self.__types

    def get_description(self):
        return self.__description

    def get_vacancies(self):
        return self.__vacancies

    def get_expiry_date(self):
        return self.__expiry_date

    def get_event_id(self):
        return self.__event_id

