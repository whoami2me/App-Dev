from flask import Flask, render_template, request, redirect, url_for
from VoucherForms import CreateVoucherForm
import shelve
import Voucher

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


@app.route('/createVoucher', methods=['GET', 'POST'])
def create_voucher():
    create_voucher_form = CreateVoucherForm(request.form)
    if request.method == 'POST' and create_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'c')

        try:
            vouchers_dict = db['Vouchers']
        except:
            print("Error in retrieving Vouchers from voucher.db.")

        voucher = Voucher.Voucher(create_voucher_form.name.data, create_voucher_form.amount.data, create_voucher_form.type.data, create_voucher_form.category.data, create_voucher_form.start.data, create_voucher_form.expiry.data, create_voucher_form.description.data)
        vouchers_dict[voucher.get_voucher_id()] = voucher
        db['Vouchers'] = vouchers_dict

        db.close()

        return redirect(url_for('retrieve_vouchers'))
    return render_template('createVoucher.html', form=create_voucher_form)


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
    update_voucher_form = CreateVoucherForm(request.form)
    if request.method == 'POST' and update_voucher_form.validate():
        vouchers_dict = {}
        db = shelve.open('voucher.db', 'w')
        vouchers_dict = db['Vouchers']

        voucher = vouchers_dict.get(id)
        voucher.set_name(update_voucher_form.name.data)
        voucher.set_amount(update_voucher_form.amount.data)
        voucher.set_type(update_voucher_form.type.data)
        voucher.set_category(update_voucher_form.category.data)
        voucher.set_start(update_voucher_form.start.data)
        voucher.set_expiry(update_voucher_form.expiry.data)
        voucher.set_description(update_voucher_form.description.data)

        db['Vouchers'] = vouchers_dict
        db.close()

        return redirect(url_for('retrieve_vouchers'))
    else:
        voucher_dict = {}
        db = shelve.open('voucher.db', 'r')
        vouchers_dict = db['Vouchers']
        db.close()

        voucher = vouchers_dict.get(id)
        update_voucher_form.name.data = voucher.get_name()
        update_voucher_form.amount.data = voucher.get_amount()
        update_voucher_form.type.data = voucher.get_type()
        update_voucher_form.category.data = voucher.get_category()
        update_voucher_form.start.data = voucher.get_start()
        update_voucher_form.expiry.data = voucher.get_expiry()
        update_voucher_form.description.data = voucher.get_description()

        return render_template('updateVoucher.html', form=update_voucher_form)


@app.route('/deleteVoucher/<int:id>', methods=['POST'])
def delete_voucher(id):
    vouchers_dict = {}
    db = shelve.open('voucher.db', 'w')
    vouchers_dict = db['Vouchers']

    vouchers_dict.pop(id)

    db['Vouchers'] = vouchers_dict
    db.close()

    return redirect(url_for('retrieve_vouchers'))


@app.route('/deleteCustomer/<int:id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customer.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)

    db['Customers'] = customers_dict
    db.close()

    return redirect(url_for('retrieve_customers'))


if __name__ == '__main__':
    app.run()
