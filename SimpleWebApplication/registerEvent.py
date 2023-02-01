
class registerEvent:
    count_id = 0

    def __init__(self, first_name, last_name, email, date_created, phone_number, event_name,status='Active'):
        registerEvent.count_id += 1
        self.__reg_user_id = registerEvent.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__status = status
        self.__date_created = date_created
        self.__phone_number = phone_number
        self.__event_name = event_name
        self.__event = None

    # accessor methods
    def get_reg_user_id(self):
        return self.__reg_user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_status(self):
        return self.__status

    def get_date_created(self):
        return self.__date_created

    def get_phone_number(self):
        return self.__phone_number

    def get_event_name(self):
        return self.__event_name

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_status(self, status):
        self.__status = status

    def set_date_created(self, date_created):
        self.__date_created = date_created

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_eve(self, event):
        self.__event = event


