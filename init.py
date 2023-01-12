from flask import Flask, render_template, request, redirect, url_for, session
from EventForms import CreateOnlineEventForm, CreateOfflineEventForm, CreateUserForm
import shelve, Events, User, OnlineEvents, OfflineEvents

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

@app.route('/createOnlineEvent', methods=['GET', 'POST'])
def create_event():
    create_online_event_form = CreateOnlineEventForm(request.form)
    if request.method == 'POST' and create_online_event_form.validate():

        online_events_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            online_events_dict = db['Events']
        except:
            print("Error in retrieving Events from event.db.")

        online_event = OnlineEvents.OnlineEvents(create_online_event_form.name.data, create_online_event_form.description.data, create_online_event_form.date.data)
        online_events_dict[online_event.get_event_id()] = online_event
        db['Events'] = online_events_dict

        db.close()

        session['online_event_created'] = online_event.get_name()

        return redirect(url_for('view_online_event'))
    return render_template('createevent.html', form=create_online_event_form)

@app.route('/createOfflineEvent', methods=['GET', 'POST'])
def create_event():
    create_offline_event_form = CreateOfflineEventForm(request.form)
    if request.method == 'POST' and create_offline_event_form.validate():

        offline_events_dict = {}
        db = shelve.open('event.db', 'c')
        try:
            offline_events_dict = db['Events']
        except:
            print("Error in retrieving Events from event.db.")

        offline_event = OfflineEvents.OfflineEvents(create_offline_event_form.name.data, create_offline_event_form.description.data, create_offline_event_form.date.data)
        offline_events_dict[offline_event.get_event_id()] = offline_event
        db['Events'] = offline_events_dict

        db.close()

        session['offline_event_created'] = offline_event.get_name()

        return redirect(url_for('view_offline_event'))
    return render_template('createevent.html', form=create_offline_event_form)


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
    online_events_dict = db['Events']
    db.close()

    online_event_list = []
    for key in online_events_dict:
        event = online_events_dict.get(key)
        online_event_list.append(event)

    return render_template('viewevent.html', count=len(online_event_list), online_event_list=online_event_list)


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
        online_events_dict = db['Events']

        event = online_events_dict.get(id)
        event.set_name(update_online_event_form.name.data)
        event.set_description(update_online_event_form.description.data)
        event.set_expiry_date(update_online_event_form.date.data)

        db['Events'] = online_events_dict
        db.close()

        session['online_event_updated'] = event.get_name()

        return redirect(url_for('view_online_event'))

    else:
        online_events_dict = {}
        db = shelve.open('event.db', 'r')
        online_events_dict = db['Events']
        db.close()

        event = online_events_dict.get(id)
        update_online_event_form.name.data = event.get_name()
        update_online_event_form.description.data = event.get_description()
        update_online_event_form.date.data = event.get_date()
        return render_template('updateevent.html', form=update_online_event_form)

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
    online_events_dict = db['Events']

    online_event = online_events_dict.pop(id)
    db['Events'] = online_events_dict
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

    return redirect(url_for('view_user'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

if __name__ == '__main__':
    app.run()
