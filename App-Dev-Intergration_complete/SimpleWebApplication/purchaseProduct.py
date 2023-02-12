class purchaseProduct:
    def __init__(self,name,id,price,userid,qty,imgname,desc):
        self.__name = name
        self.__id = id
        self.__price = price
        self.__userid = userid
        self.__qty = qty
        self.__imgname = imgname
        self.__desc = desc
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


    def set_pProduct_name(self,name):
        self.__name = name
    def set_pProduct_id(self,id):
        self.__id = id
    def set_pProduct_price(self, price):
        self.__price = price
    def set_pProduct_userid(self,userid):
        self.__userid = userid