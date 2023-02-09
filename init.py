from flask import Flask, render_template, request, redirect, url_for, session
import shelve
import Products
from ProductForms import CreateProduct, UpdateProduct, UpdateProductSale, UpdateProductImg
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/'
app.config['Product_Images_Dest'] = 'static/productimages/'



@app.route('/')
def home():
   return redirect(url_for('home_product'))


@app.route('/staff')
def staff():
    return render_template('staff.html')


@app.route('/adminevents')
def admin():
    return render_template('adminevents.html')


'''@app.route('/adminproducts')
def product():
    return render_template('adminproducts.html')'''


@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProduct(CombinedMultiDict((request.files,request.form)))

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
                             create_product_form.image.data.filename,create_product_form.sale.data)
                             
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
    update_product_form = UpdateProduct(CombinedMultiDict((request.files,request.form)))
    
    #Save changes
    if request.method == 'POST' and update_product_form.validate():
        
        products_dict = {}
        db=shelve.open('product.db','w')
        products_dict = db['Products']
       
        update_product_form.image.data.save(app.config['Product_Images_Dest'] + update_product_form.image.data.filename)
        product_id = products_dict.get(id)
        product_id.set_product_name(update_product_form.name.data) 
        product_id.set_product_price(update_product_form.price.data) 
        product_id.set_product_desc(update_product_form.desc.data) 
        product_id.set_product_qty(update_product_form.qty.data) 
        product_id.set_product_group(update_product_form.grp.data)
        product_id.set_product_image(update_product_form.image.data.filename)
        product_id.set_product_status(update_product_form.status.data)
        product_id.set_product_saleoption(update_product_form.sale.data)
        db['Products'] = products_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    #Return current product data
    else:
        products_dict = {}
        db=shelve.open('product.db','r')
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
        update_product_form.image.data = product_id.get_product_image() #Gives filename
        update_product_form.status.data = product_id.get_product_status()
        update_product_form.sale.data = product_id.get_product_saleoption()
        
        return render_template('updateProduct.html', form = update_product_form, product = product_id)

@app.route('/updateProductSale/<uuid:id>/', methods=['GET','POST'])
def update_product_sale(id):
    update_product_form = UpdateProductSale(CombinedMultiDict((request.files,request.form)))
    
    #Save changes
    if request.method == 'POST' and update_product_form.validate():
        
        products_dict = {}
        db=shelve.open('product.db','w')
        products_dict = db['Products']
       
        product_id = products_dict.get(id)
        product_id.set_product_salestartdate(update_product_form.salestartdate.data) 
        product_id.set_product_saleenddate(update_product_form.saleenddate.data) 
        product_id.set_product_saleprice(update_product_form.saleprice.data)
        db['Products'] = products_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    #Return current product data
    else:
        products_dict = {}
        db=shelve.open('product.db','r')
        products_dict = db['Products']
        db.close()
        products_list = []
        for key in products_dict:
            p = products_dict.get(key)
            products_list.append(p)

        product_id = products_dict[id]
        update_product_form.salestartdate.data = product_id.get_product_salestartdate()
        update_product_form.saleenddate.data = product_id.get_product_saleenddate()
        update_product_form.saleprice.data = product_id.get_product_saleprice1()
        
        return render_template('updateProductSale.html', form = update_product_form, product = product_id)

@app.route('/updateProductImg/<uuid:id>/', methods=['GET','POST'])
def update_product_img(id):
    update_product_form = UpdateProductImg(CombinedMultiDict((request.files,request.form)))
    
    #Save changes
    if request.method == 'POST' and update_product_form.validate():
        
        products_dict = {}
        db=shelve.open('product.db','w')
        products_dict = db['Products']
        product_id = products_dict.get(id)
        update_product_form.image.data.save(app.config['Product_Images_Dest'] + update_product_form.image.data.filename)
        product_id.set_product_image(update_product_form.image.data.filename)
        db['Products'] = products_dict
        db.close()

        return redirect(url_for('retrieve_products'))
    #Return current product data
    else:
        products_dict = {}
        db=shelve.open('product.db','r')
        products_dict = db['Products']
        db.close()
        products_list = []
        for key in products_dict:
            p = products_dict.get(key)
            products_list.append(p)

        product_id = products_dict[id]
        update_product_form.image.data = product_id.get_product_image() #Gives filename

        
        return render_template('updateProductImg.html', form = update_product_form, product = product_id)

@app.route("/deleteProduct/<uuid:id>/", methods = ["POST"])
def delete_product(id):
    products_dict = {}
    db = shelve.open('product.db','w')
    products_dict = db['Products']
    products_dict.pop(id)
    db['Products'] = products_dict
    db.close()
    return redirect(url_for('retrieve_products'))

@app.route("/homeProduct")
def home_product():
    products_dict = {}
    db = shelve.open('product.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    products_list2 = [] #Excludes inactive products

    for key in products_dict:
        p = products_dict.get(key)
        products_list.append(p)
    for i in products_list:
        if i.get_product_status() == 'Active':
            products_list2.append(i)
        
    return render_template('homeProduct.html',products = products_list2)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
