import uuid
class Product:
    def __init__(self,name,price,desc,qty,grp):
    
        self.__name = name
        self.__price = price
        self.__desc = desc
        self.__qty = qty
        self.__grp = grp
        self.__id = uuid.uuid4()
    def get_product_name(self):
        return self.__name
    def get_product_price(self):
        self.__price = float("{:.2f}".format(self.__price))
        return self.__price
    def get_product_priceformat(self):
        self.__price = ("${:.2f}".format(self.__price))
        return self.__price
    def get_product_desc(self):
        return self.__desc
    def get_product_qty(self):
        return self.__qty
    def get_product_group(self):
        return self.__grp
    def get_product_id(self):
        return self.__id

    def set_product_name(self,name):
        self.__name = name
    def set_product_price(self,price):
        self.__price = price
    def set_product_desc(self,desc):
        self.__desc = desc
    def set_product_qty(self,qty):
        self.__qty = qty
    def set_product_group(self,grp):
        self.__grp = grp
    