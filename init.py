from flask import Flask, render_template, request, redirect, url_for, session
from EventForms import CreateOnlineEventForm, CreateOfflineEventForm, CreateUserForm
from SuppliersForms import CreateSuppliersForm
import shelve, Events, User, OnlineEvents, OfflineEvents,Suppliers
import Products
from ProductForms import CreateProduct

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


@app.route('/createOnlineEvent', methods=['GET', 'POST'])
def create_event():
    create_online_event_form = CreateOnlineEventForm(request.form)
    if request.method == 'POST' and create_online_event_form.validate():

        online_events_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            online_events_dict = db['Online_Events']
        except:
            print("Error in retrieving Online Events from event.db.")

        online_event = OnlineEvents.OnlineEvents(create_online_event_form.name.data, create_online_event_form.description.data, create_online_event_form.date.data, create_online_event_form.image.data)
        online_events_dict[online_event.get_event_id()] = online_event
        db['Online_Events'] = online_events_dict

        db.close()

        session['online_event_created'] = online_event.get_name()

        return redirect(url_for('view_online_event'))
    return render_template('createevent.html', form=create_online_event_form)


@app.route('/createOfflineEvent', methods=['GET', 'POST'])
def create_offline_event():
    create_offline_event_form = CreateOfflineEventForm(request.form)
    if request.method == 'POST' and create_offline_event_form.validate():

        offline_events_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            offline_events_dict = db['Offline_Events']
        except:
            print("Error in retrieving Events from event.db.")

        offline_event = OfflineEvents.OfflineEvents(create_offline_event_form.name.data, create_offline_event_form.description.data, create_offline_event_form.date.data,
                                                    create_offline_event_form.pax.data, create_offline_event_form.location.data)
        offline_events_dict[offline_event.get_event_id()] = offline_event
        db['Offline_Events'] = offline_events_dict

        db.close()

        session['offline_event_created'] = offline_event.get_name()

        return redirect(url_for('view_offline_event'))
    return render_template('createOfflineEvent.html', form=create_offline_event_form)


@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'c')

        try:
            users_dict = db['Users']
        except:
            print("Error in retrieving Users from user.db.")

        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                         create_user_form.email.data, create_user_form.address1.data,
                         create_user_form.address2.data, create_user_form.gender.data,
                         create_user_form.membership.data)
        users_dict[user.get_user_id()] = user
        db['Users'] = users_dict
        db.close()

        session['user_created'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('view_user'))
    return render_template('createuser.html', form=create_user_form)


@app.route('/viewOnlineEvent')
def view_online_event():
    online_events_dict = {}
    db = shelve.open('event.db', 'r')
    online_events_dict = db['Online_Events']
    db.close()

    online_event_list = []
    for key in online_events_dict:
        event = online_events_dict.get(key)
        online_event_list.append(event)

    return render_template('viewevent.html', count=len(online_event_list), online_event_list=online_event_list)


@app.route('/viewofflineEvent')
def view_offline_event():
    offline_events_dict = {}
    db = shelve.open('event.db', 'r')
    offline_events_dict = db['Offline_Events']
    db.close()

    offline_event_list = []
    for key in offline_events_dict:
        event = offline_events_dict.get(key)
        offline_event_list.append(event)

    return render_template('viewOfflineEvent.html', count=len(offline_event_list), offline_event_list=offline_event_list)


@app.route('/viewuser')
def view_user():
    users_dict = {}
    db = shelve.open('user.db', 'r')
    users_dict = db['Users']
    db.close()

    user_list = []
    for key in users_dict:
        user = users_dict.get(key)
        user_list.append(user)

    return render_template('viewuser.html', count=len(user_list), user_list=user_list)


@app.route('/updateOnlineEvent/<int:id>/', methods=['GET', 'POST'])
def update_event(id):
    update_online_event_form = CreateOnlineEventForm(request.form)
    if request.method == 'POST' and update_online_event_form.validate():
        online_events_dict = {}
        db = shelve.open('event.db', 'w')
        online_events_dict = db['Online_Events']

        event = online_events_dict.get(id)
        event.set_name(update_online_event_form.name.data)
        event.set_description(update_online_event_form.description.data)
        event.set_date(update_online_event_form.date.data)

        db['Events'] = online_events_dict
        db.close()

        session['online_event_updated'] = event.get_name()

        return redirect(url_for('view_online_event'))

    else:
        online_events_dict = {}
        db = shelve.open('event.db', 'r')
        online_events_dict = db['Online_Events']
        db.close()

        event = online_events_dict.get(id)
        update_online_event_form.name.data = event.get_name()
        update_online_event_form.description.data = event.get_description()
        update_online_event_form.date.data = event.get_date()
        return render_template('updateevent.html', form=update_online_event_form)


@app.route('/updateofflineEvent/<int:id>/', methods=['GET', 'POST'])
def update_offline_event(id):
    update_offline_event_form = CreateOfflineEventForm(request.form)
    if request.method == 'POST' and update_offline_event_form.validate():
        offline_events_dict = {}
        db = shelve.open('event.db', 'w')
        offline_events_dict = db['Offline_Events']

        event = offline_events_dict.get(id)
        event.set_name(update_offline_event_form.name.data)
        event.set_description(update_offline_event_form.description.data)
        event.set_date(update_offline_event_form.date.data)
        event.set_pax(update_offline_event_form.pax.data)
        event.set_location(update_offline_event_form.location.data)

        db['Offline_Events'] = offline_events_dict
        db.close()

        session['offline_event_updated'] = event.get_name()

        return redirect(url_for('view_offline_event'))

    else:
        offline_events_dict = {}
        db = shelve.open('event.db', 'r')
        offline_events_dict = db['Offline_Events']
        db.close()

        event = offline_events_dict.get(id)
        update_offline_event_form.name.data = event.get_name()
        update_offline_event_form.description.data = event.get_description()
        update_offline_event_form.date.data = event.get_date()
        return render_template('updateevent.html', form=update_offline_event_form)


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        users_dict = {}
        db = shelve.open('user.db', 'w')
        users_dict = db['Users']

        user = users_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_address1(update_user_form.address1.data)
        user.set_address2(update_user_form.address2.data)
        user.set_gender(update_user_form.gender.data)
        user.set_membership(update_user_form.membership.data)

        db['Users'] = users_dict
        db.close()

        session['user_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('view_user'))

    else:
        users_dict = {}
        db = shelve.open('user.db', 'r')
        users_dict = db['Users']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.email.data = user.get_email()
        update_user_form.address1.data = user.get_address1()
        update_user_form.address2.data = user.get_address2()
        update_user_form.gender.data = user.get_gender()
        update_user_form.membership.data = user.get_membership()
        return render_template('updateuser.html', form=update_user_form)


@app.route('/deleteEvent/<int:id>', methods=['POST'])
def delete_event(id):
    online_events_dict = {}
    db = shelve.open('event.db', 'w')
    online_events_dict = db['Online_Events']

    online_event = online_events_dict.pop(id)
    db['Online_Events'] = online_events_dict
    db.close()

    session['event_deleted'] = online_event.get_name()

    return redirect(url_for('view_online_event'))


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    user = users_dict.pop(id)
    db['Users'] = users_dict
    db.close()

    session['user_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProduct(request.form)
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'c')
        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Product from database")
        p = Products.Product(create_product_form.name.data,create_product_form.price.data,create_product_form.desc.data,create_product_form.qty.data,create_product_form.grp.data)
        products_dict[p.get_product_id()] = p
        db['Products'] = products_dict
        db.close()
        return redirect(url_for('retrieve_products'))
    return render_template('createProduct.html', form=create_product_form)

@app.route('/retrieveProduct')
def retrieve_products():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        p = products_dict.get(key)
        products_list.append(p)
    return render_template('retrieveProduct.html', count = len(products_list), products_list = products_list, )

@app.route('/updateProduct/<uuid:id>/', methods=['GET','POST'])
def update_product(id):
    update_product_form = CreateProduct(request.form)
    if request.method == 'POST' and update_product_form.validate():

        products_dict = {}
        db=shelve.open('product.db','w')
        products_dict = db['Products']
        

        product_id = products_dict.get(id)
        product_id.set_product_name(update_product_form.name.data) 
        product_id.set_product_price(update_product_form.price.data) 
        product_id.set_product_desc(update_product_form.desc.data) 
        product_id.set_product_qty(update_product_form.qty.data) 
        product_id.set_product_group(update_product_form.grp.data) 
        db['Products'] = products_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    else:
        products_dict = {}
        db=shelve.open('product.db','r')
        products_dict = db['Products']
        db.close()

        product_id = products_dict[id]
        update_product_form.name.data = product_id.get_product_name()
        update_product_form.price.data = product_id.get_product_price()
        update_product_form.desc.data = product_id.get_product_desc()
        update_product_form.qty.data = product_id.get_product_qty()
        update_product_form.grp.data = product_id.get_product_group()
        return render_template('updateProduct.html', form = update_product_form)

@app.route("/deleteProduct/<uuid:id>/", methods = ["POST"])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db','w')
    products_dict = db['Products']
    products_dict.pop(id)
    db['Products'] = products_dict
    db.close()
    return redirect(url_for('retrieve_products'))

@app.route('/createSuppliers', methods=['GET', 'POST'])
def create_Suppliers():
    create_Supplier_form = CreateSuppliersForm(request.form)
    if request.method == 'POST' and create_Supplier_form.validate():
        Suppliers_dict = {}
        db = shelve.open('supplier.db', 'c')

        try:
            Suppliers_dict = db['Supplier']
        except:
            print("Error in retrieving Users from supplier.db.")

        supplier = Suppliers.Suppliers(create_Supplier_form.Company_name.data,create_Supplier_form.telephone.data,create_Supplier_form.website.data,create_Supplier_form.Address1.data, create_Supplier_form.Address2.data,create_Supplier_form.Payment.data,create_Supplier_form.Categories_select.data,create_Supplier_form.Product_name.data,create_Supplier_form.remarks.data)
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
        Supplier.set_set_website(update_Supplier_form.website.data)
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

@app.route('/viewSupplier/<int:id>')
def show_form(id):
    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    Suppliers_dict = db['Supplier']
    db.close()

    Supplier_list = []
    for key in Suppliers_dict:
        suppl = Suppliers_dict.get(key)
        Supplier_list.append(suppl)

    return render_template('viewSupplier.html', count=len(Supplier_list), Supplier_list=Supplier_list)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)