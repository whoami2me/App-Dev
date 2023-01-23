# User class
class Voucher:
    count_id = 0

    # initializer method
    def __init__(self, name, amount, type, category, start, expiry, description):
        Voucher.count_id += 1
        self.__type = type
        self.__voucher_id = Voucher.count_id
        self.__name = name
        self.__amount = amount
        self.__category = category
        self.__start = start
        self.__expiry = expiry
        self.__description = description

    # accessor methods
    def get_voucher_id(self):
        return self.__voucher_id

    def get_type(self):
        return self.__type

    def get_name(self):
        return self.__name

    def get_amount(self):
        return self.__amount

    def get_category(self):
        return self.__category

    def get_start(self):
        return self.__start

    def get_expiry(self):
        return self.__expiry

    def get_description(self):
        return self.__description

    # mutator methods
    def set_voucher_id(self, count_id):
        self.__voucher_id = count_id

    def set_name(self, name):
        self.__name = name

    def set_amount(self, amount):
        self.__amount = amount

    def set_category(self, category):
        self.__category = category

    def set_type(self, type):
        self.__type = type

    def set_start(self, start):
        self.__start = start

    def set_expiry(self, expiry):
        self.__expiry = expiry

    def set_description(self, description):
        self.__description = description
