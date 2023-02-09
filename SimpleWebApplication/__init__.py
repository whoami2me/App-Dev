from datetime import date
from idlelib import tooltip
from flask import Flask, render_template, request, redirect, url_for, session
from Forms import CreateEventForm, CreateOfflineEventForm, CreateOEventForm, CreateOffEventForm, UpdateCustomerForm, \
    UpdateStaffForm, CreateCustomerForm, CreateStaffForm, CreateSuppliersForm, CreateInventoryForm, RegisterEventForm
import shelve, OnlineEvents, OfflineEvents, folium, Staff, Customer, Inventory, Suppliers, registerEvent
from geopy.geocoders import Nominatim
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/'
geolocator = Nominatim(user_agent='app')


@app.route('/')
def user_home():
    session['login_user'] = 'linglong' #trisven to replace login user
    return render_template('loginevents.html')

@app.route('/AdminDashboard')
def admin_home():
    return render_template('home.html')
    
@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')

@app.route('/Events')
def events():

    online_dict = {}
    db = shelve.open('online.db', 'r')
    online_dict = db['Online']
    db.close()

    online_list = []
    for key in online_dict:
        online = online_dict.get(key)
        if online.get_date() <= date.today() <= online.get_end_date():
            print('yes')
            online_list.append(online)

    offline_dict = {}
    db = shelve.open('offline.db', 'r')
    offline_dict = db['Offline']
    db.close()

    offline_list = []
    for key in offline_dict:
        offline = offline_dict.get(key)
        if (offline.get_date() <= date.today() <= offline.get_end_date()) and (offline.get_reg_pax() < offline.get_pax()):
            offline_list.append(offline)


    return render_template('viewEvents.html', online_list=online_list, offline_list=offline_list)

@app.route('/viewRegisteredEvents')
def view_regeve():

    regeve_dict = {}
    db = shelve.open('regeve.db', 'r')
    regeve_dict = db['Register_Events']
    db.close()

    regeve_list = []
    for key in regeve_dict:
        regeve = regeve_dict.get(key)
        print(regeve.get_first_name(), session['login_user'])
        if regeve.get_first_name() == session['login_user']:
            print("the user who registered is",regeve.get_first_name())
            regeve_list.append(regeve)

    return render_template('userRegisteredEvents.html', regeve_list=regeve_list, count=len(regeve_list))



@app.route('/createOnlineEvent', methods=['GET', 'POST'])
def create_online():

    create_event_form = CreateEventForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST' and create_event_form.validate():
        online_dict = {}
        db = shelve.open('online.db', 'c')

        try:
            online_dict = db['Online']
        except:
            print("Error in retrieving Users from online.db.")

        create_event_form.image.data.save(app.config['UPLOADED_IMAGES_DEST'] + create_event_form.image.data.filename)

        today = date.today()

        online = OnlineEvents.OnlineEvents(create_event_form.name.data, create_event_form.image.data.filename, create_event_form.description.data,
                                           create_event_form.date.data, create_event_form.end_date.data ,create_event_form.location.data,'Active', 'Active', today)
        online_dict[online.get_event_id()] = online 
        db['Online'] = online_dict

        db.close()

        return redirect(url_for('retrieve_events'))
    return render_template('createEvent.html', form=create_event_form)


@app.route('/createOfflineEvent', methods=['GET', 'POST'])
def create_offline():
    create_offline_form = CreateOfflineEventForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_offline_form.validate():
        offline_dict = {}
        db = shelve.open('offline.db', 'c')

        try:
            offline_dict = db['Offline']
        except:
            print("Error in retrieving offline from offline.db.")

        create_offline_form.image.data.save(app.config['UPLOADED_IMAGES_DEST']+create_offline_form.image.data.filename)

        location = geolocator.geocode(create_offline_form.location.data)
        # Test location codes
        print(location.address)
        print((location.latitude, location.longitude))

        start_coords = (location.latitude, location.longitude)
        folium_map = folium.Map(location=start_coords, zoom_start=8)
        folium.Marker([location.latitude, location.longitude], popup=location.address, tooltip=tooltip).add_to(folium_map)
        folium_map.save('templates/map.html')

        today = date.today()

        offline = OfflineEvents.OfflineEvents(create_offline_form.name.data, create_offline_form.image.data.filename, create_offline_form.description.data,
                                              create_offline_form.date.data, create_offline_form.end_date.data ,create_offline_form.location.data, create_offline_form.pax.data,
                                              location.latitude, location.longitude, 'Active', 'Active', today)
        offline_dict[offline.get_event_id()] = offline
        db['Offline'] = offline_dict
        db.close()

        return redirect(url_for('retrieve_events'))
    return render_template('createOfflineEvent.html', form=create_offline_form)


@app.route('/registerEvents/<evename>', methods=['GET', 'POST'])
def register_event(evename):

    create_regeve_form = RegisterEventForm(request.form)

    if request.method == 'POST' and create_regeve_form.validate():

        online_dict = {}
        db = shelve.open('online.db', 'r')
        online_dict = db['Online']
        db.close()

        online_list = []
        for key in online_dict:
            online = online_dict.get(key)
            online_list.append(online)

        offline_dict = {}
        db = shelve.open('offline.db', 'r')
        offline_dict = db['Offline']
        db.close()

        offline_list = []
        for key in offline_dict:
            offline = offline_dict.get(key)
            offline_list.append(offline)

        regeve_dict = {}
        db = shelve.open('regeve.db', 'c')

        try:
            regeve_dict = db['Register_Events']
        except:
            print("Error in retrieving Registered Events from regeve.db.")

        today = date.today()

        reg_eve = registerEvent.registerEvent(create_regeve_form.first_name.data, create_regeve_form.last_name.data, create_regeve_form.email.data, today, create_regeve_form.phone_number.data, evename)

        for key in offline_list:
            if key.get_name() == evename:
                reg_eve.set_eve(key)

        for key in online_list:
            if key.get_name() == evename:
                reg_eve.set_eve(key)

        print(reg_eve.get_eve())

        regeve_dict[reg_eve.get_reg_user_id()] = reg_eve
        db['Register_Events'] = regeve_dict
        db.close()

        session['user_registered'] = reg_eve.get_first_name()
        session['event_registered'] = reg_eve.get_event_name()

        return redirect(url_for('events'))

    else:

        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        for key in customers_dict:
            customer = customers_dict.get(key)
            if customer.get_first_name() == session['login_user']:
                create_regeve_form.first_name.data = customer.get_first_name()
                create_regeve_form.last_name.data = customer.get_last_name()
                create_regeve_form.email.data = customer.get_email()
                create_regeve_form.phone_number.data = customer.get_phone_number()

            return render_template('registerEvent.html', form=create_regeve_form)


@app.route('/retrieveEvents')
def retrieve_events():

    regeve_dict = {}
    db = shelve.open('regeve.db', 'r')
    regeve_dict = db['Register_Events']
    db.close()

    regeve_list = []

    list_dict = {}
    for key in regeve_dict:
        list_dict.update({regeve_dict.get(key).get_event_name(): 0})
        if regeve_dict.get(key).get_event_name() in list_dict:
            list_dict[regeve_dict.get(key).get_event_name()] += 1

    online_dict = {}
    db = shelve.open('online.db', 'w')
    online_dict = db['Online']
    db.close()

    online_list = []
    for key in online_dict:
        online = online_dict.get(key)
        online_list.append(online)

    offline_dict = {}
    db = shelve.open('offline.db', 'r')
    offline_dict = db['Offline']
    db.close()

    offline_list = []
    for key in offline_dict:
        offline = offline_dict.get(key)
        if offline.get_name() in list_dict:
            offline.set_reg_pax(list_dict[offline.get_name()])
            offline_list.append(offline)

    return render_template('retrieveEvents.html', count=len(online_list), count1=len(offline_list), online_list=online_list, offline_list=offline_list, list_dict=list_dict)


@app.route('/updateEvent/<int:id>/', methods=['GET', 'POST'])
def update_event(id):
    update_event_form = CreateOEventForm(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST' and update_event_form.validate():
        online_dict = {}
        db = shelve.open('online.db', 'w')
        online_dict = db['Online']

        online = online_dict.get(id)
        online.set_name(update_event_form.name.data)
        online.set_description(update_event_form.description.data)
        online.set_date(update_event_form.date.data)
        online.set_end_date(update_event_form.end_date.data)
        online.set_event_status(update_event_form.event_status.data)
        online.set_reg_status(update_event_form.reg_status.data)
        online.set_image(update_event_form.image.data.filename)
        online.set_location(update_event_form.location.data)

        update_event_form.image.data.save(app.config['UPLOADED_IMAGES_DEST'] + update_event_form.image.data.filename)

        db['Online'] = online_dict
        db.close()

        return redirect(url_for('retrieve_events'))
    else:
        online_dict = {}
        db = shelve.open('online.db', 'r')
        online_dict = db['Online']
        db.close()

        online = online_dict.get(id)
        update_event_form.name.data = online.get_name()
        update_event_form.description.data = online.get_description()
        update_event_form.date.data = online.get_date()
        update_event_form.end_date.data = online.get_end_date()
        update_event_form.event_status.data = online.get_event_status()
        update_event_form.reg_status.data = online.get_reg_status()
        update_event_form.image.data = online.get_image()
        update_event_form.location.data = online.get_location()

        return render_template('updateEvent.html', form=update_event_form, online=online)


@app.route('/updateOfflineEvent/<int:id>/', methods=['GET', 'POST'])
def update_offline(id):
    update_offline_form = CreateOffEventForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and update_offline_form.validate():
        offline_dict = {}
        db = shelve.open('offline.db', 'w')
        offline_dict = db['Offline']

        offline = offline_dict.get(id)
        offline.set_name(update_offline_form.name.data)
        offline.set_description(update_offline_form.description.data)
        offline.set_date(update_offline_form.date.data)
        offline.set_end_date(update_offline_form.end_date.data)
        offline.set_pax(update_offline_form.pax.data)
        offline.set_location(update_offline_form.location.data)
        offline.set_event_status(update_offline_form.event_status.data)
        offline.set_reg_status(update_offline_form.reg_status.data)
        offline.set_image(update_offline_form.image.data.filename)

        update_offline_form.image.data.save(app.config['UPLOADED_IMAGES_DEST'] + update_offline_form.image.data.filename)

        db['Offline'] = offline_dict
        db.close()

        return redirect(url_for('retrieve_events'))
    else:
        offline_dict = {}
        db = shelve.open('offline.db', 'r')
        offline_dict = db['Offline']
        db.close()

        offline = offline_dict.get(id)
        update_offline_form.name.data = offline.get_name()
        update_offline_form.description.data = offline.get_description()
        update_offline_form.date.data = offline.get_date()
        update_offline_form.end_date.data = offline.get_end_date()
        update_offline_form.pax.data = offline.get_pax()
        update_offline_form.location.data = offline.get_location()
        update_offline_form.event_status.data = offline.get_event_status()
        update_offline_form.reg_status.data = offline.get_reg_status()
        update_offline_form.image.data = offline.get_image()

        return render_template('updateOfflineEvent.html', form=update_offline_form, offline=offline)

@app.route('/cancelRegisteredEvents/<int:id>', methods=['POST'])
def cancelEvent(id):

    regeve_dict = {}
    db = shelve.open('regeve.db', 'w')
    regeve_dict = db['Register_Events']

    user = regeve_dict.pop(id)

    db['Register_Events'] = regeve_dict
    db.close()

    session['event_cancelled'] = user.get_first_name(), 'cancelled', user.get_event_name()

    return redirect(url_for('view_regeve'))


#trisven portion

@app.route('/customerProfile')
def customer_profile():
    return render_template('customerProfile.html')

@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(request.form)
    if request.method == 'POST' and create_staff_form.validate():
        staffs_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staffs_dict = db['Staffs']
        except:
            print("Error in retrieving Staffs from staff.db.")

        today = date.today()
        staff = Staff.Staff(create_staff_form.first_name.data, create_staff_form.last_name.data,
                            create_staff_form.email.data, create_staff_form.address1.data,
                            create_staff_form.address2.data, create_staff_form.gender.data,   create_staff_form.password.data,
                            create_staff_form.passwordcfm.data, today, create_staff_form.phone_number.data,
                            create_staff_form.postal_code.data, create_staff_form.floor_number.data,
                            create_staff_form.unit_number.data)
        staffs_dict[staff.get_staff_id()] = staff
        db['Staffs'] = staffs_dict

        db.close()

        return redirect(url_for('retrieve_staffs'))
    return render_template('createStaff.html', form=create_staff_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(request.form)
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        today = date.today()
        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.email.data,
                                     create_customer_form.address1.data, create_customer_form.address2.data,
                                     create_customer_form.password.data, create_customer_form.passwordcfm.data,
                                     today, create_customer_form.phone_number.data, create_customer_form.postal_code.data,
                                     create_customer_form.floor_number.data, create_customer_form.unit_number.data)
        ##        customers_dict[customer.get_customer_id()] = customer
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict

        db.close()

        return redirect(url_for('retrieve_customers'))
    return render_template('createCustomer.html', form=create_customer_form)


@app.route('/retrieveStaffs')
def retrieve_staffs():
    staffs_dict = {}
    db = shelve.open('staff.db', 'r')
    staffs_dict = db['Staffs']
    db.close()

    staffs_list = []
    for key in staffs_dict:
        staff = staffs_dict.get(key)
        staffs_list.append(staff)

    return render_template('retrieveStaffs.html', count=len(staffs_list), staffs_list=staffs_list)


@app.route('/retrieveCustomers')
def retrieve_customers():
    customers_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        customers_list.append(customer)

    return render_template('retrieveCustomers.html', count=len(customers_list), customers_list=customers_list)


@app.route('/updateStaff/<int:id>/', methods=['GET', 'POST'])
def update_staff(id):
    update_staff_form = UpdateStaffForm(request.form)
    if request.method == 'POST' and update_staff_form.validate():
        staffs_dict = {}
        db = shelve.open('staff.db', 'w')
        staffs_dict = db['Staffs']

        staff = staffs_dict.get(id)
        staff.set_first_name(update_staff_form.first_name.data)
        staff.set_last_name(update_staff_form.last_name.data)
        staff.set_email(update_staff_form.email.data)
        staff.set_address1(update_staff_form.address1.data)
        staff.set_address2(update_staff_form.address2.data)
        staff.set_gender(update_staff_form.gender.data)
        staff.set_membership(update_staff_form.membership.data)
        staff.set_phone_number(update_staff_form.phone_number.data)
        staff.set_postal_code(update_staff_form.postal_code.data)
        staff.set_floor_number(update_staff_form.floor_number.data)
        staff.set_unit_number(update_staff_form.unit_number.data)
        staff.set_status(update_staff_form.status.data)

        db['Staffs'] = staffs_dict
        db.close()

        return redirect(url_for('retrieve_staffs'))
    else:
        staffs_dict = {}
        db = shelve.open('staff.db', 'r')
        staffs_dict = db['Staffs']
        db.close()

        staff = staffs_dict.get(id)
        update_staff_form.first_name.data = staff.get_first_name()
        update_staff_form.last_name.data = staff.get_last_name()
        update_staff_form.email.data = staff.get_email()
        update_staff_form.address1.data = staff.get_address1()
        update_staff_form.address2.data = staff.get_address2()
        update_staff_form.gender.data = staff.get_gender()
        update_staff_form.membership.data = staff.get_membership()
        update_staff_form.phone_number.data = staff.get_phone_number()
        update_staff_form.postal_code.data = staff.get_postal_code()
        update_staff_form.floor_number.data = staff.get_floor_number()
        update_staff_form.unit_number.data = staff.get_unit_number()
        update_staff_form.status.data = staff.get_status()

        return render_template('updateStaff.html', form=update_staff_form)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = UpdateCustomerForm(request.form)
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address1(update_customer_form.address1.data)
        customer.set_address2(update_customer_form.address2.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_floor_number(update_customer_form.floor_number.data)
        customer.set_unit_number(update_customer_form.unit_number.data)
        customer.set_postal_code(update_customer_form.postal_code.data)
        customer.set_status(update_customer_form.status.data)

        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('retrieve_customers'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.address1.data = customer.get_address1()
        update_customer_form.address2.data = customer.get_address2()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.floor_number.data = customer.get_floor_number()
        update_customer_form.unit_number.data = customer.get_unit_number()
        update_customer_form.postal_code.data = customer.get_postal_code()
        update_customer_form.status.data = customer.get_status()

        return render_template('updateCustomer.html', form=update_customer_form)


@app.route('/deleteStaff/<int:id>', methods=['POST'])
def delete_staff(id):
    staffs_dict = {}
    db = shelve.open('staff.db', 'w')
    staffs_dict = db['Staffs']

    staffs_dict.pop(id)

    db['Staffs'] = staffs_dict
    db.close()

    return redirect(url_for('retrieve_staffs'))


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))


@app.route('/customerLogin', methods=['GET', 'POST'])
def cslogin():
    error = None
    if request.method == 'POST':
        if request.form['Customers'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('customerHome'))
    return render_template('customerLogin.html', error=error)


@app.route('/staffLogin', methods=['GET', 'POST'])
def stafflogin():
    error = None
    if request.method == 'POST':
        if request.form['Staffs'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('dashboard'))
    return render_template('staffLogin.html', error=error)


#end of trisven portion


#start of izwan portion

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
                                       create_Supplier_form.Payment.data,create_Supplier_form.Categories_select.data,create_Supplier_form.Product_name.data,create_Supplier_form.remarks.data,
                                       today)
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
        update_Supplier_form.floor_number.data = Supplier.get_floor_number()
        update_Supplier_form.unit_number.data = Supplier.get_unit_number()
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


# end of izwan portion

@app.route('/get_map')
def get_map():
    return render_template('map.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.route('/img/<fname>')
def legacy_images(fname):
    return app.redirect(app.url_for('static', filename='uploads/' + fname), code=301)


if __name__ == '__main__':
    app.run()

