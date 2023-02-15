class Inventory:
    count_id = 0
    def __init__(self,Order_Qty,Order_remarks,date,status):
        Inventory.count_id +=1
        self.__Inventory_id = Inventory.count_id
        self.__Order_Qty = Order_Qty
        self.__Order_remarks = Order_remarks
        self.__date = date
        self.__status = status

    def get_Inventory_id(self):
        return self.__Inventory_id
    def get_Order_Qty(self):
        return self.__Order_Qty
    #def get_status(self):
    #    return self.__status
    def get_Order_remarks(self):
        return self.__Order_remarks
    def get_date(self):
        return self.__date
    def get_status(self):
        return self.__status
    def set_Inventory_id(self, Inventory_id):
        self.__Inventory_id = Inventory_id
    def set_Order_Qty(self,Order_Qty):
        self.__Order_Qty = Order_Qty
    #def set_status(self,status):
     #   self.__status = status
    def set_Order_remarks(self,Order_remarks):
        self.__Order_remarks = Order_remarks
    def set_date(self,date):
        self.__date = date
    def set_status(self,status):
        self.__status = status

