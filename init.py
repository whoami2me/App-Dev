from flask import Flask, render_template, request, redirect, url_for, session
from EventForms import CreateOnlineEventForm, CreateOfflineEventForm, CreateUserForm
from SuppliersForms import CreateSuppliersForm
from InventoryForms import CreateInventoryForm
import shelve, Events, User, OnlineEvents, OfflineEvents,Suppliers,Inventory
import Products
from ProductForms import CreateProduct
from datetime import date
app = Flask(__name__)
app.secret_key = 'any_random_string'
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']


@app.route('/')
def home():
    return render_template('loginevents.html')


@app.route('/staff')
def staff():
    return render_template('staff.html')


@app.route('/adminevents')
def admin():
    return render_template('adminevents.html')


@app.route('/adminproducts')
def product():
    return render_template('adminproducts.html')

@app.route('/createSuppliers', methods=['GET', 'POST'])
def create_Suppliers():
    create_Supplier_form = CreateSuppliersForm(request.form)
    if request.method == 'POST' and create_Supplier_form.validate():
        Suppliers_dict = {}
        db = shelve.open('supplier.db', 'c')

        try:
            Suppliers_dict = db['Supplier']
        except:
            print("Error in retrieving info from supplier.db.")
        today = date.today()
        supplier = Suppliers.Suppliers(create_Supplier_form.Company_name.data,create_Supplier_form.telephone.data,create_Supplier_form.website.data,create_Supplier_form.email.data,create_Supplier_form.Address1.data, create_Supplier_form.Address2.data,create_Supplier_form.postal.data,create_Supplier_form.Payment.data,create_Supplier_form.Categories_select.data,create_Supplier_form.Product_name.data,create_Supplier_form.remarks.data, today)
        Suppliers_dict[supplier.get_Suppliers_id()] = supplier
        db['Supplier'] = Suppliers_dict

        db.close()

        return redirect(url_for('retrieve_Supplier'))
    return render_template('createSuppliers.html', form=create_Supplier_form)

@app.route('/retrieveSupplier')
def retrieve_Supplier():
    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    Suppliers_dict = db['Supplier']
    db.close()

    Suppliers_list = []
    for key in Suppliers_dict:
        supp = Suppliers_dict.get(key)
        Suppliers_list.append(supp)

    return render_template('retrieveSupplier.html', count=len(Suppliers_list), Suppliers_list=Suppliers_list)

@app.route('/updateSupplier/<int:id>/', methods=['GET', 'POST'])
def update_Supplier(id):
    update_Supplier_form = CreateSuppliersForm(request.form)
    if request.method == 'POST' and update_Supplier_form.validate():
        Suppliers_dict = {}
        db = shelve.open('supplier.db', 'w')
        try:
            Suppliers_dict = db['Supplier']
        except:
            print("Error in retrieving Users from supplier.db for updating")

        Supplier = Suppliers_dict.get(id)
        Supplier.set_Company_name(update_Supplier_form.Company_name.data)
        Supplier.set_telephone(update_Supplier_form.telephone.data)
        Supplier.set_website(update_Supplier_form.website.data)
        Supplier.set_email(update_Supplier_form.email.data)
        Supplier.set_Address1(update_Supplier_form.Address1.data)
        Supplier.set_Address2(update_Supplier_form.Address2.data)
        Supplier.set_Payment(update_Supplier_form.Payment.data)
        Supplier.set_Categories_select(update_Supplier_form.Categories_select.data)
        Supplier.set_Product_name(update_Supplier_form.Product_name.data)
        Supplier.set_remarks(update_Supplier_form.remarks.data)

        db['Supplier'] = Suppliers_dict
        db.close()

        return redirect(url_for('retrieve_Supplier'))
    else:
        Suppliers_dict = {}
        db = shelve.open('supplier.db', 'r')
        try:
            Suppliers_dict = db['Supplier']
        except:
            print("Error in retrieving Users from supplier.db for closing")

        db.close()

        Supplier = Suppliers_dict.get(id)
        update_Supplier_form.Company_name.data = Supplier.get_Company_name()
        update_Supplier_form.telephone.data = Supplier.get_telephone()
        update_Supplier_form.website.data = Supplier.get_website()
        update_Supplier_form.email.data = Supplier.get_email()
        update_Supplier_form.Address1.data = Supplier.get_Address1()
        update_Supplier_form.Address2.data = Supplier.get_Address2()
        update_Supplier_form.Payment.data = Supplier.get_Payment()
        update_Supplier_form.Categories_select.data = Supplier.get_Categories_select()
        update_Supplier_form.Product_name.data = Supplier.get_Product_name()
        update_Supplier_form.remarks.data = Supplier.get_remarks()

        return render_template('updateSupplier.html', form=update_Supplier_form)

@app.route('/deleteSupplier/<int:id>', methods=['POST'])
def delete_Supplier(id):
    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'w')
    Suppliers_dict = db['Supplier']

    Suppliers_dict.pop(id)

    db['Supplier'] = Suppliers_dict
    db.close()

    return redirect(url_for('retrieve_Supplier'))

@app.route('/createInventory', methods=['GET', 'POST'])
def create_Inventory():
    create_Inventory_form = CreateInventoryForm(request.form)
    if request.method == 'POST' and create_Inventory_form.validate():
        Inventory_dict = {}
        db = shelve.open('Inventory.db', 'c')

        try:
            Inventory_dict = db['Inventory']
        except:
            print("Error in retrieving supply from Inventory.db.")
        today = date.today()
        supply = Inventory.Inventory(create_Inventory_form.Categories_select.data,create_Inventory_form.Product_name.data,create_Inventory_form.Qty.data,create_Inventory_form.remarks.data ,today)
        Inventory_dict[Inventory.get_Inventory_id()] = supply
        db['Inventory'] = Inventory_dict

        db.close()

        return redirect(url_for('retrieve_Inventory'))
    return render_template('createInventory.html', form=create_Inventory_form)

@app.route('/retrieveInventory')
def retrieve_Inventory():
    Inventory_dict = {}
    db = shelve.open('Inventory.db', 'r')
    Inventory_dict = db['Inventory']
    db.close()

    Inventory_list = []
    for key in Inventory_dict:
        supp = Inventory_dict.get(key)
        Inventory_list.append(supp)

    return render_template('retrieveInventory.html', count=len(Inventory_list), Inventory_list=Inventory_list)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
