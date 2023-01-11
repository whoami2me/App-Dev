from flask import Flask, render_template, request, redirect, url_for, session
from EventForms import CreateEventForm, CreateUserForm
import shelve, Events, User

app = Flask(__name__)
app.secret_key = 'any_random_string'


@app.route('/')
def home():
    return render_template('loginevents.html')

@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/adminevents')
def admin():
    return render_template('adminevents.html')

@app.route('/createevent', methods=['GET', 'POST'])
def create_event():
    create_event_form = CreateEventForm(request.form)
    if request.method == 'POST' and create_event_form.validate():

        events_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            events_dict = db['Events']
        except:
            print("Error in retrieving Events from event.db.")

        event = Events.Events(create_event_form.name.data, create_event_form.types.data, create_event_form.description.data,
                              create_event_form.vacancies.data, create_event_form.expiry_date.data)
        events_dict[event.get_event_id()] = event
        db['Events'] = events_dict

        db.close()

        session['event_created'] = event.get_name()

        return redirect(url_for('view_event'))
    return render_template('createevent.html', form=create_event_form)


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

@app.route('/viewevent')
def view_event():
    events_dict = {}
    db = shelve.open('event.db', 'r')
    events_dict = db['Events']
    db.close()

    event_list = []
    for key in events_dict:
        event = events_dict.get(key)
        event_list.append(event)

    return render_template('viewevent.html', count=len(event_list), event_list=event_list)


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


@app.route('/updateEvent/<int:id>/', methods=['GET', 'POST'])
def update_event(id):
    update_event_form = CreateEventForm(request.form)
    if request.method == 'POST' and update_event_form.validate():
        events_dict = {}
        db = shelve.open('event.db', 'w')
        events_dict = db['Events']

        event = events_dict.get(id)
        event.set_name(update_event_form.name.data)
        event.set_types(update_event_form.types.data)
        event.set_description(update_event_form.description.data)
        event.set_vacancies(update_event_form.vacancies.data)
        event.set_expiry_date(update_event_form.expiry_date.data)

        db['Events'] = events_dict
        db.close()

        session['event_updated'] = event.get_name()

        return redirect(url_for('view_event'))

    else:
        events_dict = {}
        db = shelve.open('event.db', 'r')
        events_dict = db['Events']
        db.close()

        event = events_dict.get(id)
        update_event_form.name.data = event.get_name()
        update_event_form.types.data = event.get_types()
        update_event_form.description.data = event.get_description()
        update_event_form.vacancies.data = event.get_vacancies()
        update_event_form.expiry_date.data = event.get_expiry_date()
        return render_template('updateevent.html', form=update_event_form)

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
    events_dict = {}
    db = shelve.open('event.db', 'w')
    events_dict = db['Events']

    event = events_dict.pop(id)
    db['Events'] = events_dict
    db.close()

    session['event_deleted'] = event.get_name()

    return redirect(url_for('view_event'))


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    users_dict = {}
    db = shelve.open('user.db', 'w')
    users_dict = db['Users']

    user = users_dict.pop(id)
    db['Users'] = users_dict
    db.close()

    session['user_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

    return redirect(url_for('view_user'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

if __name__ == '__main__':
    app.run()
