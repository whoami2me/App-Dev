class Suppliers:
    count_id = 0
    def __init__(self,Company_name,telephone,website,email,Address1,Address2,postal,Payment,Categories_select,Product_name,remarks,date):
        Suppliers.count_id +=1
        self.__Suppliers_id = Suppliers.count_id
        self.__Company_name = Company_name
        self.__telephone = telephone
        self.__website = website
        self.__email = email
        self.__Address1 = Address1
        self.__Address2 = Address2
        self.__postal = postal
        self.__Payment = Payment
        self.__Categories_select = Categories_select
        self.__Product_name = Product_name
        self.__remarks = remarks
        self.__date = date
    def get_Suppliers_id(self):
        return self.__Suppliers_id
    def get_Company_name(self):
        return self.__Company_name
    def get_telephone(self):
        return self.__telephone
    def get_website(self):
        return self.__website
    def get_email(self):
        return self.__email
    def get_Address1(self):
        return self.__Address1
    def get_Address2(self):
        return self.__Address2
    def get_postal(self):
        return self.__postal
    def get_Payment(self):
        return self.__Payment
    def get_Categories_select(self):
        return self.__Categories_select
    def get_Product_name(self):
        return self.__Product_name
    def get_remarks(self):
        return self.__remarks
    def get_date(self):
        return self.__date

    def set_Suppliers_id(self, Suppliers_id):
        self.__Suppliers_id = Suppliers_id
    def set_Company_name(self,Company_name):
        self.__Company_name = Company_name
    def set_telephone(self,telephone):
        self.__telephone = telephone
    def set_website(self,website):
        self.__website = website
    def set_email(self,email):
        self.__email = email
    def set_Address1(self,Address1):
        self.__Address1 = Address1
    def set_Address2(self,Address2):
        self.__Address2 = Address2
    def set_postal(self,postal):
        self.__postal = postal
    def set_Payment(self,Payment):
        self.__Payment = Payment
    def set_Categories_select(self,Categories_select):
        self.__Categories_select = Categories_select
    def set_Product_name(self,Product_name):
        self.__Product_name = Product_name
    def set_remarks(self,remarks):
        self.__remarks = remarks
    def set_date(self,date):
        self.__date = date
