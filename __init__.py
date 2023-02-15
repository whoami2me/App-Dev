from datetime import date, datetime
from idlelib import tooltip
from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from Forms import CreateEventForm, CreateOfflineEventForm, CreateOEventForm, CreateOffEventForm, UpdateCustomerForm, \
    UpdateStaffForm, CreateCustomerForm, CreateStaffForm, RegisterEventForm, \
    Login, UpdateProduct, CreateProduct, UpdateProductSale, UpdateProductImg, PurchaseProduct, ChangePassword, \
    CreateVoucherForm
from SuppliersForms import CreateSuppliersForm
from InventoryForms import CreateInventoryForm
import shelve, OnlineEvents, OfflineEvents, folium,  registerEvent, pdfkit, Products, purchaseProduct, json, Staff, Customer, Voucher, Inventory, Suppliers
from geopy.geocoders import Nominatim
from werkzeug.datastructures import CombinedMultiDict
import re

app = Flask(__name__)
#path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
#config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/'
app.config['Product_Images_Dest'] = 'static/productimages/'
app.config['UPLOADED_PROFILE_IMAGES_DEST'] = 'static/ProfilePic/'

geolocator = Nominatim(user_agent='app')

@app.route('/')
def user_home():

    if session.get('name') is not None:
        print(session['name'])
    else:
        session['name'] = 'client'
    return render_template('loginevents.html')

@app.route('/AdminDashboard')
def admin_home():

    regeve_dict = {}
    db = shelve.open('regeve.db', 'r')
    regeve_dict = db['Register_Events']
    db.close()

    list_dict = {}

    for key in regeve_dict:
        list_dict.update({regeve_dict.get(key).get_event_name(): 0})

    for key in regeve_dict:
        if regeve_dict.get(key).get_event_name() in list_dict:
            list_dict[regeve_dict.get(key).get_event_name()] += 1

    events = []
    registered = []

    for keys in list_dict:
        events.append(keys)
        registered.append(list_dict[keys])


    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    redvouch_dict = {}
    db = shelve.open('save.db', 'r')
    redvouch_dict = db['redeemed']
    db.close()

    used_dict = {}
    db = shelve.open('used.db', 'r')
    used_dict = db['used']
    db.close()

    count_dict = {}
    for i in vouchers_dict:
        count = 0
        count1 = 0
        print(i)

        for key in used_dict:
            if i == int(key):
                print(f"They are equal, {len(used_dict[key])}")
                usedcount = len(used_dict[key])
                count += usedcount
                count1 += usedcount
        print(count)
        count_dict.update({i:count1})
    keysList = list(count_dict.keys())
    countList = list(count_dict.values())

    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    productname_list = []
    productsales_list = []
    totalsold_list = []
    producttotalsales = 0
    for key in products_dict:
        productobj = products_dict.get(key)
        productname = productobj.get_product_name()
        productsales = productobj.get_total_earned2()
        totalsold = productobj.get_product_sold()

        productsalesnum = float(re.sub('[^0-9.]', '', productsales))
        producttotalsales += productsalesnum
        productname_list.append(productname)
        productsales_list.append(productsalesnum)
        totalsold_list.append(totalsold)
    producttotalsales = "${:.2f}".format(producttotalsales)
    print(producttotalsales)
    

    return render_template('home.html', events=json.dumps(events), reg_pax=json.dumps(registered), keysList=json.dumps(keysList), countList=json.dumps(countList), productname=json.dumps(productname_list), productsales=json.dumps(productsales_list), producttotalsales=json.dumps(producttotalsales),producttotalsold=json.dumps(totalsold_list))


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
        if (online.get_date() <= date.today() <= online.get_end_date()) and (
                online.get_reg_status() == 'Active' or online.get_reg_status() == 'A'):
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

    regeve_list = []
    list_dict = {}

    if session['name'] != 'client':

        regeve_dict = {}
        db = shelve.open('regeve.db', 'r')
        regeve_dict = db['Register_Events']
        db.close()


        for key in regeve_dict:
                regeve = regeve_dict.get(key)
                if regeve.get_first_name() == session['name']:
                    regeve_list.append(regeve.get_event_name())

        for key in regeve_dict:
            list_dict.update({regeve_dict.get(key).get_event_name(): 0})

        for key in regeve_dict:
            if regeve_dict.get(key).get_event_name() in list_dict:
                list_dict[regeve_dict.get(key).get_event_name()] += 1

        db = shelve.open('offline.db', 'w')
        offline_dict = db['Offline']

        offline_list = []
        for key in offline_dict:
            offline = offline_dict.get(key)
            if (offline.get_date() <= date.today() <= offline.get_end_date()) and (
                    offline.get_reg_pax() < offline.get_pax()) and (
                    offline.get_reg_status() == 'Active' or offline.get_reg_status() == 'A'):
                    if offline.get_name() in list_dict:
                        offline.set_reg_pax(list_dict[offline.get_name()])
                        offline_list.append(offline)
                    else:
                        offline.set_reg_pax(0)
                        offline_list.append(offline)

        db['Offline'] = offline_dict
        db.close()

    return render_template('viewEvents.html', online_list=online_list, offline_list=offline_list, regeve_list=regeve_list, user=session['name'])


@app.route('/viewDetails/<evename>')
def vev_details(evename):

    online_dict = {}
    db = shelve.open('online.db', 'r')
    online_dict = db['Online']
    db.close()

    online_list = []
    for key in online_dict:
        online = online_dict.get(key)
        if online.get_name() == evename:
            online_list.append(online)

    offline_dict = {}
    db = shelve.open('offline.db', 'r')
    offline_dict = db['Offline']
    db.close()

    offline_list = []
    for key in offline_dict:
        offline = offline_dict.get(key)
        if offline.get_name() == evename:
            offline_list.append(offline)

    return render_template('viewdetailseve.html', offline_list=offline_list, online_list=online_list)

@app.route('/viewRegisteredEvents')
def view_regeve():

    regeve_dict = {}
    db = shelve.open('regeve.db', 'r')
    regeve_dict = db['Register_Events']
    db.close()

    regeve_list = []
    for key in regeve_dict:
        regeve = regeve_dict.get(key)
        print(regeve.get_first_name(), )
        if regeve.get_first_name() == session['name']:
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

        session['registered_Event'] = session['name'] + "have registered" + evename

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
            if customer.get_first_name() == session['name']:
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

    for key in regeve_dict:
        if regeve_dict.get(key).get_event_name() in list_dict:
            list_dict[regeve_dict.get(key).get_event_name()] += 1

    online_dict = {}
    db = shelve.open('online.db', 'r')
    online_dict = db['Online']
    db.close()

    online_list = []
    for key in online_dict:
        online = online_dict.get(key)
        online_list.append(online)

    offline_dict = {}
    db = shelve.open('offline.db', 'w')
    offline_dict = db['Offline']


    offline_list = []
    for key in offline_dict:
        offline = offline_dict.get(key)

        if offline.get_name() in list_dict:
            offline.set_reg_pax(list_dict[offline.get_name()])
        else:
            offline.set_reg_pax(0)
        offline_list.append(offline)

    db['Offline'] = offline_dict
    db.close()


    return render_template('retrieveEvents.html', count=len(online_list), count1=len(offline_list), online_list=online_list, offline_list=offline_list)


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

    session['event_cancelled'] = user.get_first_name() + 'cancelled' + user.get_event_name()

    return redirect(url_for('view_regeve'))


#start of trisven portion


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login(request.form)
    customers_dict = {}
    staff_dict = {}
    db = shelve.open('customer.db', 'r')
    customers_dict = db['Customers']
    db.close()
    db = shelve.open('staff.db', 'r')
    staff_dict = db['Staffs']
    db.close()
    for email in customers_dict:
        customer = customers_dict.get(email)
        if customer.get_email() == login_form.email.data and customer.get_password() == login_form.password.data:
            session['Customer'] = customer.get_customer_id()
            session['name'] = customer.get_first_name()
            session['image'] = customer.get_image()
            if customer.get_status() == 'Active':
                return redirect(url_for('user_home'))
            else:
                flash('Account has been blocked.', 'error')
                redirect('login')
        if customer.get_email() != login_form.email.data or customer.get_password() != login_form.password.data:
            flash('login failed', 'fail')
            redirect('login')

    for email in staff_dict:
        staff = staff_dict.get(email)
        if staff.get_email() == login_form.email.data and staff.get_password() == login_form.password.data:
            session['Staff'] = staff.get_staff_id()
            session['name'] = staff.get_first_name()
            session['image'] = staff.get_image()
            session['membership'] = staff.get_membership()
            if staff.get_status() == 'Active':
                return redirect(url_for('admin_home'))
            else:
                flash('Account has been blocked.', 'error')
                redirect('login')
        if staff.get_email() != login_form.email.data or staff.get_password() != login_form.password.data:
            flash('login failed', 'fail')
            redirect('login')
    return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    session.pop('Customer', None)
    session.pop('Staff', None)
    session.pop('name', None)

    return redirect(url_for('user_home'))

@app.route('/profile/<int:id>/', methods=['GET', 'POST'])
def profile_page(id):
    update_customer_form = UpdateCustomerForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address1(update_customer_form.address1.data)
        customer.set_address2(update_customer_form.address2.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_postal_code(update_customer_form.postal_code.data)
        customer.set_floor_number(update_customer_form.floor_number.data)
        customer.set_unit_number(update_customer_form.unit_number.data)
        customer.set_image(update_customer_form.image.data.filename)

        update_customer_form.image.data.save(
            app.config['UPLOADED_PROFILE_IMAGES_DEST'] + update_customer_form.image.data.filename)

        db['Customers'] = customers_dict
        db.close()
        session['image'] = customer.get_image()
        flash('Profile has been updated!', 'profileSuccess')
        return redirect(url_for('user_home'))
    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        update_customer_form.first_name.data = customer.get_first_name()
        update_customer_form.last_name.data = customer.get_last_name()
        update_customer_form.email.data = customer.get_email()
        update_customer_form.address1.data = customer.get_address1()
        update_customer_form.address2.data = customer.get_address2()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.postal_code.data = customer.get_postal_code()
        update_customer_form.floor_number.data = customer.get_floor_number()
        update_customer_form.unit_number.data = customer.get_unit_number()
        update_customer_form.image.data = customer.get_image()
        session['image'] = customer.get_image()

        return render_template('customerProfilePage.html', form=update_customer_form, customer=customer)


@app.route('/changepassword/<int:id>/', methods=['GET', 'POST'])
def customer_change_password(id):
    customer_change_password_form = ChangePassword(request.form)
    if request.method == 'POST' and customer_change_password_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_password(customer_change_password_form.password.data)
        customer.set_passwordcfm(customer_change_password_form.passwordcfm.data)

        db['Customers'] = customers_dict
        db.close()
        flash('Password has been changed!', 'passwordSuccess')
        return redirect(url_for('user_home'))

    else:
        customers_dict = {}
        db = shelve.open('customer.db', 'r')
        customers_dict = db['Customers']
        db.close()

        customer = customers_dict.get(id)
        customer_change_password_form.password.data = customer.get_password()
        customer_change_password_form.passwordcfm.data = customer.get_passwordcfm()

    return render_template('customerChangePassword.html', form=customer_change_password_form)

@app.route('/staffchangepassword/<int:id>/', methods=['GET', 'POST'])
def staff_change_password(id):
    staff_change_password_form = ChangePassword(request.form)
    if request.method == 'POST' and staff_change_password_form.validate():
        staffs_dict = {}
        db = shelve.open('staff.db', 'w')
        staffs_dict = db['Staffs']

        staff = staffs_dict.get(id)
        staff.set_password(staff_change_password_form.password.data)
        staff.set_passwordcfm(staff_change_password_form.passwordcfm.data)

        db['Staffs'] = staffs_dict
        db.close()
        flash('Password has been changed!', 'passwordSuccess')
        return redirect(url_for('admin_home'))

    else:
        staffs_dict = {}
        db = shelve.open('staff.db', 'r')
        staffs_dict = db['Staffs']
        db.close()

        staff = staffs_dict.get(id)
        staff_change_password_form.password.data = staff.get_password()
        staff_change_password_form.passwordcfm.data = staff.get_passwordcfm()

    return render_template('staffChangePassword.html', form=staff_change_password_form)


@app.route('/staffprofile/<int:id>/', methods=['GET', 'POST'])
def staff_profile_page(id):
    update_staff_form = UpdateStaffForm(CombinedMultiDict((request.files, request.form)))
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
        staff.set_image(update_staff_form.image.data.filename)

        update_staff_form.image.data.save(
            app.config['UPLOADED_PROFILE_IMAGES_DEST'] + update_staff_form.image.data.filename)

        db['Staffs'] = staffs_dict
        db.close()

        flash('Profile has been updated!', 'profileSuccess')
        session['image'] = staff.get_image()
        return redirect(url_for('admin_home'))
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
        update_staff_form.image.data = staff.get_image()
        session['image'] = staff.get_image()

        return render_template('staffProfilePage.html', form=update_staff_form, staff=staff)

@app.route('/createStaff', methods=['GET', 'POST'])
def create_staff():
    create_staff_form = CreateStaffForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_staff_form.validate():
        staffs_dict = {}
        db = shelve.open('staff.db', 'c')

        try:
            staffs_dict = db['Staffs']
        except:
            print("Error in retrieving Staffs from staff.db.")

        create_staff_form.image.data.save(app.config['UPLOADED_PROFILE_IMAGES_DEST'] + create_staff_form.image.data.filename)

        today = date.today()
        staff = Staff.Staff(create_staff_form.first_name.data, create_staff_form.last_name.data,
                            create_staff_form.email.data, create_staff_form.address1.data,
                            create_staff_form.address2.data, create_staff_form.gender.data, create_staff_form.password.data,
                            create_staff_form.passwordcfm.data, today, create_staff_form.phone_number.data,
                            create_staff_form.postal_code.data, create_staff_form.floor_number.data,
                            create_staff_form.unit_number.data, create_staff_form.image.data.filename)
        staffs_dict[staff.get_staff_id()] = staff
        db['Staffs'] = staffs_dict

        db.close()

        return redirect(url_for('retrieve_staffs'))
    return render_template('createStaff.html', form=create_staff_form)


@app.route('/createCustomer', methods=['GET', 'POST'])
def create_customer():
    create_customer_form = CreateCustomerForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("Error in retrieving Customers from customer.db.")

        create_customer_form.image.data.save(app.config['UPLOADED_PROFILE_IMAGES_DEST'] + create_customer_form.image.data.filename)

        today = date.today()
        customer = Customer.Customer(create_customer_form.first_name.data, create_customer_form.last_name.data,
                                     create_customer_form.gender.data, create_customer_form.email.data,
                                     create_customer_form.address1.data, create_customer_form.address2.data,
                                     create_customer_form.password.data, create_customer_form.passwordcfm.data,
                                     today, create_customer_form.phone_number.data, create_customer_form.postal_code.data,
                                     create_customer_form.floor_number.data, create_customer_form.unit_number.data,
                                     create_customer_form.image.data.filename)
        ##        customers_dict[customer.get_customer_id()] = customer
        customers_dict[customer.get_customer_id()] = customer
        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('login'))
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
    update_staff_form = UpdateStaffForm(CombinedMultiDict((request.files, request.form)))
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
        staff.set_image(update_staff_form.image.data.filename)

        update_staff_form.image.data.save(app.config['UPLOADED_PROFILE_IMAGES_DEST'] + update_staff_form.image.data.filename)

        db['Staffs'] = staffs_dict
        session['image'] = staff.get_image()
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
        update_staff_form.image.data = staff.get_image()
        session['image'] = staff.get_image()

        return render_template('updateStaff.html', form=update_staff_form, staff=staff)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = UpdateCustomerForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and update_customer_form.validate():
        customers_dict = {}
        db = shelve.open('customer.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(update_customer_form.first_name.data)
        customer.set_last_name(update_customer_form.last_name.data)
        customer.set_email(update_customer_form.email.data)
        customer.set_address1(update_customer_form.address1.data)
        customer.set_address2(update_customer_form.address2.data)
        customer.set_gender(update_customer_form.gender.data)
        customer.set_phone_number(update_customer_form.phone_number.data)
        customer.set_postal_code(update_customer_form.postal_code.data)
        customer.set_floor_number(update_customer_form.floor_number.data)
        customer.set_unit_number(update_customer_form.unit_number.data)
        customer.set_status(update_customer_form.status.data)
        customer.set_image(update_customer_form.image.data.filename)

        update_customer_form.image.data.save(
            app.config['UPLOADED_PROFILE_IMAGES_DEST'] + update_customer_form.image.data.filename)

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
        update_customer_form.email.data = customer.get_email()
        update_customer_form.address1.data = customer.get_address1()
        update_customer_form.address2.data = customer.get_address2()
        update_customer_form.gender.data = customer.get_gender()
        update_customer_form.phone_number.data = customer.get_phone_number()
        update_customer_form.postal_code.data = customer.get_postal_code()
        update_customer_form.floor_number.data = customer.get_floor_number()
        update_customer_form.unit_number.data = customer.get_unit_number()
        update_customer_form.status.data = customer.get_status()
        update_customer_form.image.data = customer.get_image()

        return render_template('updateCustomer.html', form=update_customer_form, customer=customer)

#end of trisven portion


#start of azami portion

@app.route("/clearDb", methods=["POST", "GET"])
def clear_db():
    voucher_dict = {}
    db = shelve.open('save.db', 'w')
    voucher_dict = db['redeemed']

    used_dict = {}
    a = shelve.open("used.db", "c")
    used_dict = a["used"]

    used_dict.clear()
    voucher_dict.clear()

    db['redeemed'] = voucher_dict
    a["used"] = used_dict

    db.close()
    a.close()

    return redirect(url_for('retrieve_vouchers'))

@app.route('/useVoucher/<vouid>', methods=['POST'])
def use_voucher(vouid):
    voucher_dict = {}
    db = shelve.open('save.db', 'w')
    voucher_dict = db['redeemed']

    names = voucher_dict[vouid]
    print(names)
    print(session["name"])
    index = names.index(session["name"])
    print(index)
    names.pop(index)
    print(names)
    voucher_dict[vouid] = names
    db["redeemed"] = voucher_dict
    db.close()

    vouchers = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    used_dict = {}
    a = shelve.open("used.db", "c")
    used_dict = a["used"]
    print(used_dict)
    if vouid in used_dict:
        list = used_dict[vouid]
        print(list)
        list.append(session["name"])
        print(session['name'])
        used_dict[vouid] = list
    else:
        used_dict.update({vouid: [session["name"]]})
    print(used_dict)

    for k in used_dict:
        a[k] = used_dict[k]
    print(f"final used: {used_dict}")
    a["used"] = used_dict

    return redirect(url_for('retrieve_vouchers_account'))


@app.route('/redeemVoucher/<vouid>', methods=['GET', 'POST'])
def redeem_voucher(vouid):
        vouchers = {}
        db = shelve.open('voucher.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()

        vouchers_list = []
        for key in vouchers_dict:
            voucher = vouchers_dict.get(key)
            vouchers_list.append(voucher)

        redeemed_dict = {}
        a = shelve.open("save.db", "c")
        redeemed_dict = a["redeemed"]
        print(redeemed_dict)
        if vouid in redeemed_dict:
            list = redeemed_dict[vouid]
            print(list)
            list.append(session["name"])
            redeemed_dict[vouid] = list
        else:
            redeemed_dict.update({vouid: [session["name"]]})
        print(redeemed_dict)

        for k in redeemed_dict:
                a[k] = redeemed_dict[k]
        print(redeemed_dict)
        a["redeemed"] = redeemed_dict

        return redirect(url_for('retrieve_vouchers_account'))


@app.route('/createVoucher', methods=['GET', 'POST'])
def create_voucher():
    create_voucher_form = CreateVoucherForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and create_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'c')

        try:
            vouchers_dict = db['Vouchers']
        except:
            print("Error in retrieving Vouchers from voucher.db.")

        voucher = Voucher.Voucher(create_voucher_form.picture.data, create_voucher_form.name.data, create_voucher_form.type.data, create_voucher_form.amount.data, create_voucher_form.min_spend.data, create_voucher_form.category.data, create_voucher_form.start.data, create_voucher_form.expiry.data, create_voucher_form.description.data, create_voucher_form.status.data)
        vouchers_dict[voucher.get_voucher_id()] = voucher
        db['Vouchers'] = vouchers_dict

        db.close()

        return redirect(url_for('retrieve_vouchers'))
    return render_template('createVoucher.html', form=create_voucher_form)

@app.route('/retrieveVouchersAccount', methods=["GET", "POST"])
def retrieve_vouchers_account():
    redvouch_dict = {}
    db = shelve.open('save.db', 'r')
    redvouch_dict = db['redeemed']
    db.close()

    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()


    redvouch_list = []
    for key in redvouch_dict:
        redvouch = redvouch_dict.get(key)
        if session["name"] in redvouch:
            print("the user who registered is", session["name"])
            redvouch_list.append(key)

    print(redvouch_list)
    vouchers_list2 = []
    for key in redvouch_list:
        key1 = int(key)
        voucher = vouchers_dict.get(key1)
        vouchers_list2.append(voucher)

    return render_template('retrieveVouchersCustomer.html', count=len(vouchers_list2), vouchers_list=vouchers_list2, vouchers_list2=vouchers_list2)

@app.route('/retrieveVouchersCustomer', methods=["GET", "POST"])
def retrieve_vouchers_customer():
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    redvouch_dict = {}
    db = shelve.open('save.db', 'r')
    redvouch_dict = db['redeemed']
    db.close()

    used_dict = {}
    db = shelve.open('used.db', 'r')
    used_dict = db['used']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    vouchers_list1 = []
    for i in vouchers_list:
        if i.get_status() == 'Active' and i.get_expiry() >= datetime.date(datetime.now()) and i.get_start() <= datetime.date(datetime.now()):
            vouchers_list1.append(i)

    redvouch_list = []
    for key in redvouch_dict:
        redvouch = redvouch_dict.get(key)
        if session["name"] in redvouch:
            print("the user who registered is", session["name"])
            redvouch_list.append(key)

    print(redvouch_list)
    vouchers_list2 = []
    for key in redvouch_list:
        key1 = int(key)
        voucher = vouchers_dict.get(key1)
        vouchers_list2.append(voucher)

    used_list = []
    for key in used_dict:
        usedvoucher = used_dict.get(key)
        if session["name"] in usedvoucher:
            print("the user who registered is", session["name"])
            used_list.append(key)

    print(used_list)
    vouchers_list3 = []
    for key in used_list:
        key1 = int(key)
        voucher = vouchers_dict.get(key1)
        vouchers_list3.append(voucher)

    return render_template('retrieveVouchersCustomer.html', count=len(vouchers_list1), vouchers_list=vouchers_list1, vouchers_list2=vouchers_list2, vouchers_list3=vouchers_list3)


@app.route('/retrieveVouchers')
def retrieve_vouchers():
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'r')
    vouchers_dict = db['Vouchers']
    db.close()

    vouchers_list = []
    for key in vouchers_dict:
        voucher = vouchers_dict.get(key)
        vouchers_list.append(voucher)

    return render_template('retrieveVouchers.html', count=len(vouchers_list), vouchers_list=vouchers_list)


@app.route('/updateVoucher/<int:id>/', methods=['GET', 'POST'])
def update_voucher(id):
    update_voucher_form = CreateVoucherForm(CombinedMultiDict((request.files, request.form)))
    if request.method == 'POST' and update_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'w')
        vouchers_dict = db['Vouchers']

        voucher = vouchers_dict.get(id)
        voucher.set_picture(update_voucher_form.picture.data)
        voucher.set_name(update_voucher_form.name.data)
        voucher.set_type(update_voucher_form.type.data)
        voucher.set_amount(update_voucher_form.amount.data)
        voucher.set_min_spend(update_voucher_form.min_spend.data)
        voucher.set_category(update_voucher_form.category.data)
        voucher.set_start(update_voucher_form.start.data)
        voucher.set_expiry(update_voucher_form.expiry.data)
        voucher.set_description(update_voucher_form.description.data)
        voucher.set_status(update_voucher_form.status.data)

        db['Vouchers'] = vouchers_dict
        db.close()

        return redirect(url_for('retrieve_vouchers'))
    else:
        voucher_dict = {}
        db = shelve.open('voucher.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()

        voucher = vouchers_dict.get(id)
        update_voucher_form.picture.data = voucher.get_picture()
        update_voucher_form.name.data = voucher.get_name()
        update_voucher_form.type.data = voucher.get_type()
        update_voucher_form.amount.data = voucher.get_amount()
        update_voucher_form.min_spend.data = voucher.get_min_spend()
        update_voucher_form.category.data = voucher.get_category()
        update_voucher_form.start.data = voucher.get_start()
        update_voucher_form.expiry.data = voucher.get_expiry()
        update_voucher_form.description.data = voucher.get_description()
        update_voucher_form.status.data = voucher.get_status()

        return render_template('updateVoucher.html', form=update_voucher_form)


@app.route('/deleteVoucher/<int:id>', methods=['POST'])
def delete_voucher(id):
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'w')
    vouchers_dict = db['Vouchers']

#end of azami portion



# start of rayden portion

@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProduct(CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'c')
        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Product from database")

        create_product_form.image.data.save(app.config['Product_Images_Dest'] + create_product_form.image.data.filename)

        p = Products.Product(create_product_form.name.data,
                             create_product_form.price.data,
                             create_product_form.desc.data,
                             create_product_form.qty.data,
                             create_product_form.grp.data,
                             create_product_form.image.data.filename, create_product_form.sale.data)

        products_dict[p.get_product_id()] = p
        db['Products'] = products_dict
        db.close()
        session['product_created'] = ("ID:{} | Name:{}".format(p.get_product_id(), p.get_product_name()))
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

    return render_template('retrieveProduct.html', count=len(products_list), products_list=products_list, )


@app.route('/updateProduct/<uuid:id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = UpdateProduct(CombinedMultiDict((request.files, request.form)))

    # Save changes
    if request.method == 'POST' and update_product_form.validate():

        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product_id = products_dict.get(id)
        product_id.set_product_name(update_product_form.name.data)
        product_id.set_product_price(update_product_form.price.data)
        product_id.set_product_desc(update_product_form.desc.data)
        product_id.set_product_qty(update_product_form.qty.data)
        product_id.set_product_group(update_product_form.grp.data)
        product_id.set_product_status(update_product_form.status.data)
        product_id.set_product_saleoption(update_product_form.sale.data)
        db['Products'] = products_dict
        db.close()
        session['product_updated'] = (
            "ID:{} | Name:{}".format(product_id.get_product_id(), product_id.get_product_name()))
        return redirect(url_for('retrieve_products'))
    # Return current product data
    else:
        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()
        products_list = []
        for key in products_dict:
            p = products_dict.get(key)
            products_list.append(p)

        product_id = products_dict[id]
        update_product_form.name.data = product_id.get_product_name()
        update_product_form.price.data = product_id.get_product_price()
        update_product_form.desc.data = product_id.get_product_desc()
        update_product_form.qty.data = product_id.get_product_qty()
        update_product_form.grp.data = product_id.get_product_group()
        update_product_form.status.data = product_id.get_product_status()
        update_product_form.sale.data = product_id.get_product_saleoption()

        return render_template('updateProduct.html', form=update_product_form, product=product_id)


@app.route('/updateProductSale/<uuid:id>/', methods=['GET', 'POST'])
def update_product_sale(id):
    update_product_form = UpdateProductSale(CombinedMultiDict((request.files, request.form)))
    # Save changes
    if request.method == 'POST' and update_product_form.validate():

        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']

        product_id = products_dict.get(id)
        product_id.set_product_salestartdate(update_product_form.salestartdate.data)
        product_id.set_product_saleenddate(update_product_form.saleenddate.data)
        product_id.set_product_saleprice(update_product_form.saleprice.data)
        db['Products'] = products_dict
        db.close()
        session['product_updated'] = (
            "ID:{} | Name:{}".format(product_id.get_product_id(), product_id.get_product_name()))
        return redirect(url_for('retrieve_products'))
    # Return current product data
    else:
        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        product_id = products_dict[id]
        update_product_form.salestartdate.data = product_id.get_product_salestartdate()
        update_product_form.saleenddate.data = product_id.get_product_saleenddate()
        update_product_form.saleprice.data = product_id.get_product_saleprice1()
        return render_template('updateProductSale.html', form=update_product_form, product=product_id)


@app.route('/updateProductImg/<uuid:id>/', methods=['GET', 'POST'])
def update_product_img(id):
    update_product_form = UpdateProductImg(CombinedMultiDict((request.files, request.form)))

    # Save changes
    if request.method == 'POST' and update_product_form.validate():

        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']
        product_id = products_dict.get(id)
        update_product_form.image.data.save(app.config['Product_Images_Dest'] + update_product_form.image.data.filename)
        product_id.set_product_image(update_product_form.image.data.filename)
        db['Products'] = products_dict
        db.close()
        session['product_updated'] = (
            "ID:{} | Name:{}".format(product_id.get_product_id(), product_id.get_product_name()))
        return redirect(url_for('retrieve_products'))
    # Return current product data
    else:
        products_dict = {}
        db = shelve.open('product.db', 'r')
        products_dict = db['Products']
        db.close()

        product_id = products_dict[id]
        update_product_form.image.data = product_id.get_product_image()  # Gives filename

        return render_template('updateProductImg.html', form=update_product_form, product=product_id)


@app.route("/deleteProduct/<uuid:id>/", methods=["POST"])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']
    p = products_dict.pop(id)
    db['Products'] = products_dict
    db.close()
    session['product_deleted'] = ("ID:{} | Name:{}".format(p.get_product_id(), p.get_product_name()))
    return redirect(url_for('retrieve_products'))


@app.route("/homeProduct")
def home_product():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()
    products_list = []
    products_list2 = []  # Excludes inactive products
    products_list3 = []  # Excludes active products

    for key in products_dict:
        p = products_dict.get(key)
        products_list.append(p)
    for i in products_list:
        if i.get_product_status() == 'Active':
            products_list2.append(i)
    for i in products_list:
        if i.get_product_status() == 'Inactive':
            products_list3.append(i)

    return render_template('homeProduct.html', products=products_list2, products2=products_list3)


@app.route("/singleProduct/<uuid:id>/", methods=['GET', 'POST'])
def single_product(id):
    purchase_product_form = PurchaseProduct(CombinedMultiDict((request.files, request.form)))
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()
    p = products_dict.get(id)
    
    if isinstance(session.get('Customer'),int):
        logincheck = 'True'
    else:
        logincheck = 'False'
    
    print(logincheck)
 

    if request.method == 'POST' and purchase_product_form.validate():
        products_dict = {}
        db = shelve.open('product.db', 'w')
        products_dict = db['Products']
        product_id = products_dict.get(id)
        if purchase_product_form.qty.data > product_id.get_product_qty():  # Validate user input if more than stock
            purchase_product_form.qty.errors.append('Quantity selected was more than stock')
            return render_template('singleProduct.html', product=p, form=purchase_product_form,logincheck = logincheck)
        
        if purchase_product_form.option.data == 'Purchase':
            purchaseproducts_dict = {}
            totalsold = product_id.get_product_sold() + purchase_product_form.qty.data
            product_id.set_product_sold(totalsold)
            qtyremaning = product_id.get_product_qty() - purchase_product_form.qty.data
            product_id.set_product_qty(qtyremaning)
            db['Products'] = products_dict
            db.close()
            db = shelve.open('purchaseproduct.db', 'c')
            try:
                purchaseproducts_dict = db['purchaseProducts']
            except:
                print("Error in retrieving Product from database")
            if product_id.get_product_saleoption() == 'Active':
                price = product_id.get_product_saleprice()
                price2 = product_id.get_product_saleprice2()
            else:
                price = "${:.2f}".format(product_id.get_product_price())
                price2 = "${}".format(product_id.get_product_price())
            
            numericprice = re.sub('[^0-9.]', '', price2)
            calctotalprice = float(numericprice) * float(purchase_product_form.qty.data)
            totalprice = "${:.2f}".format(calctotalprice)
            custpurchase = purchaseProduct.purchaseProduct(product_id.get_product_name(), product_id.get_product_id(),
                                                           price, session['Customer'], purchase_product_form.qty.data,
                                                           product_id.get_product_image(),
                                                           product_id.get_product_desc(), totalprice)

            purchaseproducts_dict[custpurchase.get_tempvar()] = custpurchase

            db['purchaseProducts'] = purchaseproducts_dict
            db.close()
            products_dict = {}
            db = shelve.open('product.db', 'w')
            products_dict = db['Products']
            product_id = products_dict.get(id)
            totalearned = product_id.get_total_earned() + calctotalprice
            product_id.set_total_earned(totalearned)
            db['Products'] = products_dict
            db.close()

            return render_template('purchaseProduct.html', product=p, pqty=purchase_product_form.qty.data)
        elif purchase_product_form.option.data == 'Add to cart':
            addproduct_dict = {}
            db = shelve.open('addproduct.db', 'c')
            try:
                addproduct_dict = db['addProducts']
            except:
                print("Error in retrieving product from database")
            if product_id.get_product_saleoption() == 'Active':
                price = product_id.get_product_saleprice()
                price2 = product_id.get_product_saleprice2()
            else:
                price = "${:.2f}".format(product_id.get_product_price())
                price2 = "${}".format(product_id.get_product_price())

            numericprice = re.sub('[^0-9.]', '', price2)
            calctotalprice = float(numericprice) * float(purchase_product_form.qty.data)
            totalprice = "${:.2f}".format(calctotalprice)
            custpurchase = purchaseProduct.purchaseProduct(product_id.get_product_name(), product_id.get_product_id(),
                                                           price, session['Customer'], purchase_product_form.qty.data,
                                                           product_id.get_product_image(),
                                                           product_id.get_product_desc(), totalprice)

            addproduct_dict[custpurchase.get_tempvar()] = custpurchase
            print(custpurchase.get_tempvar())
            db['addProducts'] = addproduct_dict
            db.close()
            return render_template('addcartProduct.html', product=p, pqty=purchase_product_form.qty.data)
        else:
            print('Error')
    return render_template('singleProduct.html', product=p, form=purchase_product_form,logincheck = logincheck)


@app.route('/viewpurchaseProduct')
def viewpurchaseproduct():
    purchaseproductdict = {}
    db = shelve.open('purchaseproduct.db', 'r')
    purchaseproductdict = db['purchaseProducts']
    db.close()
    customer_list = []

    
    for key in purchaseproductdict:  # Key is tempvar (uuid)
        purchaseproduct = purchaseproductdict.get(key)
        if purchaseproduct.get_pProduct_userid() == session['Customer']:
            customer_list.append(purchaseproduct)
   

    return render_template('viewpurchaseproduct.html', customer=customer_list)


@app.route('/viewcartProduct')
def viewcartproduct():
    addproductdict = {}
    db = shelve.open('addproduct.db', 'r')
    addproductdict = db['addProducts']
    db.close()
    customer_list = []
    for key in addproductdict:  # Key is tempvar (uuid)
        purchaseproduct = addproductdict.get(key)
        print(key)
        if purchaseproduct.get_pProduct_userid() == session['Customer']:
            customer_list.append(purchaseproduct)

    
    return render_template('viewcartProduct.html', customer=customer_list)


@app.route('/purchasecartProduct/<uuid:id>/')
def purchasecartproduct(id):
    db = shelve.open('addproduct.db', 'r')
    addproductdict = db['addProducts']
    db.close()

    purchaseproductdict = {}
    db = shelve.open('purchaseproduct.db', 'w')
    purchaseproductdict = db['purchaseProducts']

    productcartobj = addproductdict.get(id)
    print(productcartobj)
    purchaseproductdict[id] = productcartobj
    db['purchaseProducts'] = purchaseproductdict
    db.close()

    products_dict = {}
    db = shelve.open('product.db', 'w')
    products_dict = db['Products']
    product_id = productcartobj.get_pProduct_id()
    productobj = products_dict.get(product_id)
    totalsold = productobj.get_product_sold() + productcartobj.get_pProduct_qty()
    productobj.set_product_sold(totalsold)
    qtyremaining = productobj.get_product_qty() - productcartobj.get_pProduct_qty()
    productobj.set_product_qty(qtyremaining)
    calctotalpricestr = productcartobj.get_pProduct_totalprice()
    calctotalpricenum = re.sub('[^0-9.]', '', calctotalpricestr)
    totalearned = productobj.get_total_earned() + float(calctotalpricenum)
    productobj.set_total_earned(totalearned)
    db['Products'] = products_dict
    db.close()

    db = shelve.open('addproduct.db', 'w')
    addproductdict = db['addProducts']
    addproductdict.pop(id)
    db['addProducts'] = addproductdict
    db.close()
    return redirect(url_for('home_product'))


@app.route('/removecartProduct/<uuid:id>/', methods=['POST'])
def removecartproduct(id):
    db = shelve.open('addproduct.db', 'w')
    addproductdict = db['addProducts']
    p = addproductdict.get(id)
    addproductdict.pop(id)
    db['addProducts'] = addproductdict
    db.close()
    return redirect(url_for('viewcartproduct'))


# end of rayden portion



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
        Inventory_list=[]
        db = shelve.open('inventory.db', 'c')
        try:
            Inventory_dict = db['inventory']
        except:
            print("Error in retrieving supply from Inventory.db.")
        today = date.today()
        supply = Inventory.Inventory(create_Inventory_form.Order_Qty.data,create_Inventory_form.Order_remarks.data,today,'Processing')

        Inventory_dict[supply.get_Inventory_id()] = supply
        db['inventory'] = Inventory_dict
        db.close()
        Supply = Inventory_dict.get(id)
        Inventory_list.append(Supply)


        return redirect(url_for('retrieve_Inventory'))
    return render_template('createInventory.html', form=create_Inventory_form,Suppliers_list=Suppliers_list)


@app.route('/retrieveInventory')
def retrieve_Inventory():
    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    Suppliers_dict = db['Supplier']
    db.close()

    Suppliers_list = []
    for key in Suppliers_dict:
        supp = Suppliers_dict.get(key)
        Suppliers_list.append(supp)

    inventory_dict = {}
    db = shelve.open('inventory.db', 'r')
    inventory_dict = db['inventory']
    db.close()

    Inventory_list = []
    for key in inventory_dict:
        Supply = inventory_dict.get(key)
        Inventory_list.append(Supply)


    # Retrieve the inventory dictionary

    return render_template('retrieveInventory.html', count=len(Inventory_list),Suppliers_list=Suppliers_list,Inventory_list=Inventory_list)


@app.route("/invoice/<int:id>")
def invoice(id):
    Inventory_dict = {}
    db = shelve.open('inventory.db', 'r')
    Inventory_dict = db['inventory']
    Inventory_dict.get(id)
    db.close()

    Inventory_list = []
    for key in Inventory_dict:
        supply = Inventory_dict.get(key)
        Inventory_list.append(supply)

    Suppliers_dict = {}
    db = shelve.open('supplier.db', 'r')
    Suppliers_dict = db['Supplier']
    db.close()

    Suppliers_list = []
    for key in Suppliers_dict:
        supp = Suppliers_dict.get(key)
        Suppliers_list.append(supp)

    return render_template("invoice.html", Inventory_list=Inventory_list, Suppliers_list=Suppliers_list)

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

@app.route('/profimg/<fname>')
def profile_images(fname):
    return app.redirect(app.url_for('static', filename='ProfilePic/' + fname), code=301)

'''@app.route("/getPDF/<evename>")
def get_pdf(evename):

    regeve_dict = {}
    db = shelve.open('regeve.db', 'r')
    regeve_dict = db['Register_Events']
    db.close()

    regeve_list = []
    for key in regeve_dict:
        regeve = regeve_dict.get(key)
        if evename == regeve.get_event_name():
            regeve_list.append(regeve)

    html = render_template("registeredList.html", regeve_list=regeve_list, count_users=len(regeve_list))
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=registeredUserLists.pdf"

    return response'''


if __name__ == '__main__':
    app.run(debug=True)

