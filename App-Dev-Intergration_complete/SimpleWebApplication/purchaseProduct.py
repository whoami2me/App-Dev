import uuid
from datetime import date
class purchaseProduct:
    def __init__(self,name,id,price,userid,qty,imgname,desc,totalprice):
        self.__name = name
        self.__id = id
        self.__price = price
        self.__userid = userid
        self.__qty = qty
        self.__imgname = imgname
        self.__desc = desc
        self.__tempvar = uuid.uuid4() #For saving as key in purchaseProduct db 
        self.__date = date.today()
        self.__totalprice = totalprice
    def get_pProduct_name(self):
        return self.__name
    def get_pProduct_id(self):
        return self.__id
    def get_pProduct_price(self):
        return self.__price
    def get_pProduct_userid(self):
        return self.__userid
    def get_pProduct_qty(self):
        return self.__qty
    def get_pProduct_image(self):
        return self.__imgname
    def get_pProduct_desc(self):
        return self.__desc
    def get_tempvar(self):
        return self.__tempvar
    def get_pProduct_date(self):
        return self.__date
    def get_pProduct_totalprice(self):
        return self.__totalprice


    def set_pProduct_name(self,name):
        self.__name = name
    def set_pProduct_id(self,id):
        self.__id = id
    def set_pProduct_price(self, price):
        self.__price = price
    def set_pProduct_userid(self,userid):
        self.__userid = userid