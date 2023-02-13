class Inventory:
    counting_id = 0
    def __init__(self,Product_name,Company_name,type,Qty,remarks,date):
        Inventory.counting_id +=1
        self.__Inventory_id = Inventory.counting_id
        self.__Product_name = Product_name
        self.__Company_name = Company_name
        self.__type = type
        self.__Qty = Qty
        self.__remarks = remarks
        self.__date = date

    def get_Inventory_id(self):
        return self.__Inventory_id
    def get_Product_name(self):
        return self.__Product_name
    def get_Company_name(self):
        return self.__Company_name
    def get_type(self):
        return self.__type
    def get_Qty(self):
        return self.__Qty
    #def get_status(self):
    #    return self.__status
    def get_remarks(self):
        return self.__remarks
    def get_date(self):
        return self.__date

    def set_Inventory_id(self, Inventory_id):
        self.__Inventory_id = Inventory_id
    def set_Product_name(self,Product_name):
        self.__Product_name = Product_name
    def set_Company_name(self,Company_name):
        self.__Company_name = Company_name
    def set_type(self,type):
        self.__type = type
    def set_Qty(self,Qty):
        self.__Qty = Qty
    #def set_status(self,status):
     #   self.__status = status
    def set_remarks(self,remarks):
        self.__remarks = remarks
    def set_date(self,date):
        self.__date = date


