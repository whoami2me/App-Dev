# User class
class Voucher:
    count_id = 0

    # initializer method
    def __init__(self, picture, name, type, amount, min_spend, category, start, expiry, description, status):
        Voucher.count_id += 1
        self.__voucher_id = Voucher.count_id
        self.__picture = picture
        self.__name = name
        self.__type = type
        self.__amount = amount
        self.__min_spend = min_spend
        self.__category = category
        self.__start = start
        self.__expiry = expiry
        self.__description = description
        self.__status = status

    # accessor methods
    def get_voucher_id(self):
        return self.__voucher_id

    def get_type(self):
        return self.__type

    def get_picture(self):
        return self.__picture

    def get_min_spend(self):
        return self.__min_spend

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

    def get_status(self):
        return self.__status

    # mutator methods
    def set_voucher_id(self, count_id):
        self.__voucher_id = count_id

    def set_picture(self, picture):
        self.__picture = picture

    def set_name(self, name):
        self.__name = name

    def set_min_spend(self, min_spend):
        self.__min_spend = min_spend

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

    def set_status(self, status):
        self.__status = status


class redeemVoucher:
    count_id = 0

    def __init__(self, voucher_id, name):
        redeemVoucher.count_id += 1
        self.__redeemVoucher_id = redeemVoucher.count_id
        self.__red_name = name
        self.__voucher_id = voucher_id
        self.__voucher = None

    def set_voucher_id(self, voucher_id):
        self.__voucher_id = voucher_id

    def get_voucher_id(self):
        return self.__voucher_id

    def set_voucher(self, voucher):
        self.__voucher = voucher

    def set_red_name(self, name):
        self.__red_name = name

    def get_red_name(self):
        return self.__red_name

