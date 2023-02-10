import uuid
from datetime import date, datetime
class Product:
    def __init__(self,name,price,desc,qty,grp,image,saleoption=None,status='Active',priceclass='item high col-md-4',salestartdate=date.today(),saleenddate=date.today(),saleprice=0):
    
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
        self.__salepoption = saleoption
        self.__salestartdate = salestartdate
        self.__saleenddate = saleenddate
        self.__saleprice = saleprice
    def get_product_name(self):
        return self.__name
    def get_product_price(self):
        return self.__price
    def get_product_priceformat(self):
        self.__price2 = ("${:.2f}".format(float(self.__price)))
        return self.__price2
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
        if self.__qty <=0:
            self.__status = 'Inactive'
        return self.__status
    def get_product_priceclass(self):
        self.__saleprice2 = float(self.__price)-(float(self.__price)*float(self.__saleprice/100))
        if self.__status == 'Inactive':
            self.__priceclass = 'item new col-md-4'
        else:
            if self.__salepoption == 'Yes':
                if self.__saleprice2 <= 100:
                    self.__priceclass = 'item low col-md-4'
                else:
                    self.__priceclass = 'item high col-md-4'
            else:
                if self.__price <=100:
                    self.__priceclass = 'item low col-md-4'
                else:
                    self.__priceclass = 'item high col-md-4'
        return self.__priceclass
    def get_product_saleoption(self):
        return self.__salepoption
    def get_product_salestartdate(self):
        return self.__salestartdate
    def get_product_saleenddate(self):
        return self.__saleenddate 
    def get_product_saleprice(self):
        salepercent = self.__saleprice
        self.__saleprice2 = float(self.__price)-(float(self.__price)*float(self.__saleprice/100))
        return ('${:.2f} (Discount: {}%)'.format(self.__saleprice2,salepercent))
    def get_product_saleprice1(self):
        return self.__saleprice
        
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
    def set_product_saleoption(self,saleoption):
        self.__salepoption = saleoption
    def set_product_salestartdate(self,salestartdate):
        self.__salestartdate = salestartdate
    def set_product_saleenddate(self,saleenddate):
        self.__saleenddate = saleenddate
    def set_product_saleprice(self,saleprice):
        self.__saleprice = saleprice