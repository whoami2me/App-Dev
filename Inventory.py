class Inventory:
    counting_id = 0
    def __init__(self,Qty,remarks,date):
        Inventory.counting_id +=1
        self.__Inventory_id = Inventory.counting_id
        self.__Qty = Qty
        self.__remarks = remarks
        self.__date = date

    def get_Inventory_id(self):
        return self.__Inventory_id
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
    def set_Qty(self,Qty):
        self.__Qty = Qty
    #def set_status(self,status):
     #   self.__status = status
    def set_remarks(self,remarks):
        self.__remarks = remarks
    def set_date(self,date):
        self.__date = date


