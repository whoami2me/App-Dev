from Suppliers import *
class Inventory(Suppliers):
    count_id = 0
    def __init__(self,Categories_select,Product_name,Qty,status,):
        super().__init__(Categories_select,Product_name)
        Inventory.count_id +=1
        self.__Qty = Qty
        self.__status = status

    def get_Qty(self):
        return self.__Qty
    def get_status(self):
        return self.__status

    def set_Qty(self,Qty):
        self.__Qty = Qty
    def set_status(self,status):
        self.__status = status
