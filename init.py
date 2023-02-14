from flask import Flask, render_template, request, redirect, url_for
from SuppliersForms import CreateSuppliersForm
from InventoryForms import CreateInventoryForm
import shelve,Suppliers,Inventory
from datetime import date


app = Flask(__name__)
app.secret_key = 'any_random_string'
app.config['UPLOAD_DIRECTORY'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif']


@app.route('/')
def home():
    return render_template('loginevents.html')

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
        supplier = Suppliers.Suppliers(create_Supplier_form.Company_name.data,create_Supplier_form.telephone.data,create_Supplier_form.website.data,create_Supplier_form.email.data,
                                       create_Supplier_form.Address1.data, create_Supplier_form.floor_number.data,create_Supplier_form.unit_number.data,create_Supplier_form.postal.data,
                                       create_Supplier_form.Payment.data,create_Supplier_form.Categories_select.data,create_Supplier_form.Product_name.data,create_Supplier_form.price.data,create_Supplier_form.Qty.data,create_Supplier_form.remarks.data,
                                       today, 'Available')
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
        Supplier.set_floor_number(update_Supplier_form.floor_number.data)
        Supplier.set_unit_number(update_Supplier_form.unit_number.data)
        Supplier.set_postal(update_Supplier_form.postal.data)
        Supplier.set_Payment(update_Supplier_form.Payment.data)
        Supplier.set_Categories_select(update_Supplier_form.Categories_select.data)
        Supplier.set_Product_name(update_Supplier_form.Product_name.data)
        Supplier.set_price(update_Supplier_form.price.data)
        Supplier.set_Qty(update_Supplier_form.Qty.data)
        Supplier.set_remarks(update_Supplier_form.remarks.data)
        Supplier.set_status(update_Supplier_form.status.data)


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
        update_Supplier_form.floor_number.data = Supplier.get_floor_number()
        update_Supplier_form.unit_number.data = Supplier.get_unit_number()
        update_Supplier_form.postal.data = Supplier.get_postal()
        update_Supplier_form.Payment.data = Supplier.get_Payment()
        update_Supplier_form.Categories_select.data = Supplier.get_Categories_select()
        update_Supplier_form.Product_name.data = Supplier.get_Product_name()
        update_Supplier_form.price.data = Supplier.get_price()
        update_Supplier_form.Qty.data = Supplier.get_Qty()
        update_Supplier_form.remarks.data = Supplier.get_remarks()
        update_Supplier_form.status.data = Supplier.get_status()

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


@app.route('/createInventory/<int:id>', methods=['GET', 'POST'])
def create_Inventory(id):
    create_Inventory_form = CreateInventoryForm(request.form)
    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    Suppliers_dict = db['Supplier']
    db.close()
    Suppliers_list=[]
    Supplier = Suppliers_dict.get(id)
    Suppliers_list.append(Supplier)

    if request.method == 'POST' and create_Inventory_form.validate():
        Inventory_dict = {}
        db = shelve.open('inventory.db', 'c')
        try:
            Inventory_dict = db['inventory']
        except:
            print("Error in retrieving supply from Inventory.db.")
        today = date.today()
        supply = Inventory.Inventory(create_Inventory_form.Qty.data,create_Inventory_form.remarks.data,today)

        Inventory_dict[supply.get_Inventory_id()] = supply
        db['inventory'] = Inventory_dict

        db.close()

        return redirect(url_for('retrieve_Inventory'))
    return render_template('createInventory.html', form=create_Inventory_form,Suppliers_list=Suppliers_list)

def Combine():
    suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    suppliers_dict = db['Supplier']
    db.close()

    inventory_dict = {}
    db = shelve.open('inventory.db', 'r')
    inventory_dict = db['inventory']
    db.close()

    combined_db = shelve.open('combined.db', 'c')
    combined_db['suppliers'] = suppliers_dict
    combined_db['inventory'] = inventory_dict
    combined_db.close()

@app.route('/retrieveInventory')
def retrieve_Inventory():
    Combine()

    combine_dict = {}
    db = shelve.open('combined.db', 'r')
    try:
        combine_dict = db['combine']
    except:
        print("Error in retrieving supply from combined.db.")
    db.close()

    combine_list = []
    supply = combine_dict.get(id)
    combine_list.append(supply)
    print(combine_list)

    return render_template('retrieveInventory.html', count=len(combine_list), combine_list=combine_list)


@app.route("/invoice/<int:id>")
def invoice(id):
    Inventory_dict = {}

    db = shelve.open('inventory.db', 'r')
    Inventory_dict = db['inventory']
    Inventory_dict.get(id)
    db.close()


    Inventory_list = []
    for key in Inventory_dict:
        suply = Inventory_dict.get(key)
        Inventory_list.append(suply)

    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    Suppliers_dict = db['Supplier']
    db.close()

    Suppliers_list = []
    for key in Suppliers_dict:
        supp = Suppliers_dict.get(key)
        Suppliers_list.append(supp)

    return render_template("invoice.html", Inventory_list=Inventory_list, Suppliers_list=Suppliers_list)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
