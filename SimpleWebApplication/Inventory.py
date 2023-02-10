class Inventory:

    count_id = 0
    def __init__(self,Categories_select,Product_name,Qty,remarks,date):

        Inventory.count_id +=1
        self.__Inventory_id = Inventory.count_id
        self.__Categories_select = Categories_select
        self.__Product_name = Product_name
        self.__Qty = Qty
        self.__remarks = remarks
        self.__date = date

    def get_Inventory_id(self):
        return self.__Inventory_id
    def get_Categories_select(self):
        return self.__Categories_select
    def get_Product_name(self):
        return self.__Product_name
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
    def set_Categories_select(self,Categories_select):
        self.__Categories_select = Categories_select
    def set_Product_name(self,Product_name):
        self.__Product_name = Product_name
    def set_Qty(self,Qty):
        self.__Qty = Qty
    #def set_status(self,status):
     #   self.__status = status
    def set_remarks(self,remarks):
        self.__remarks = remarks
    def set_date(self,date):
        self.__date = date
