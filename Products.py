import uuid
from datetime import date
class Product:
    def __init__(self,name,price,desc,qty,grp,image,status='Active',priceclass='item high col-md-4',saledate='Nil'):
    
        self.__name = name
        self.__price = price
        self.__desc = desc
        self.__qty = qty
        self.__grp = grp
        self.__id = uuid.uuid4()
        self.__date = date.today()
        self.__image = image
        self.__status = status
        self.__priceclass = priceclass
        self.__saledate = saledate
    def get_product_name(self):
        return self.__name
    def get_product_price(self):
        self.__price = float("{:.2f}".format(self.__price))
        return self.__price
    def get_product_priceformat(self):
        self.__price = ("${:.2f}".format(float(self.__price)))
        return self.__price
    def get_product_desc(self):
        return self.__desc
    def get_product_qty(self):
        return self.__qty
    def get_product_group(self):
        self.__grp=(','.join(self.__grp))
        return self.__grp
    def get_product_id(self):
        return self.__id
    def get_product_date(self):
        return self.__date
    def get_product_image(self):
        return self.__image
    def get_product_status(self):
        return self.__status
    def get_product_priceclass(self):
        if self.__price <=100:
            self.__priceclass = 'item low col-md-4'
        return self.__priceclass

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
    def set_product_image(self,image):
        self.__image = image
    def set_product_status(self,status):
        self.__status = status