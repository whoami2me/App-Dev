from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateStaffForm, CreateCustomerForm
import shelve, Staff, Customer
from datetime import date

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('customerHome.html')

@app.route('/customerProfile')
def customer_profile():
    return render_template('customerProfile.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


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
                            create_staff_form.address2.data, create_staff_form.gender.data,
                            create_staff_form.membership.data,  create_staff_form.password.data,
                            create_staff_form.passwordcfm.data, 'Active', today, create_staff_form.phone_number.data)
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
                                     'Active', today, create_customer_form.phone_number.data)
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
    update_staff_form = CreateStaffForm(request.form)
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
        staff.set_password(update_staff_form.password.data)
        staff.set_passwordcfm(update_staff_form.passwordcfm.data)
        staff.set_phone_number(update_staff_form.phone_number.data)

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
        update_staff_form.password.data = staff.get_password()
        update_staff_form.passwordcfm.data = staff.get_passwordcfm()
        update_staff_form.phone_number.data = staff.get_phone_number()

        return render_template('updateStaff.html', form=update_staff_form)


@app.route('/updateCustomer/<int:id>/', methods=['GET', 'POST'])
def update_customer(id):
    update_customer_form = CreateCustomerForm(request.form)
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

##@app.route('/staff/changePasswordStaff')


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


if __name__ == '__main__':
    app.run()
