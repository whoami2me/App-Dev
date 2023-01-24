from datetime import date
from idlelib import tooltip
from flask import Flask, render_template, request, redirect, url_for
from Forms import CreateEventForm, CreateOfflineEventForm, CreateOEventForm, CreateOffEventForm
import shelve, OnlineEvents, OfflineEvents, folium
from geopy.geocoders import Nominatim
from werkzeug.datastructures import CombinedMultiDict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisisasecret'
app.config['UPLOADED_IMAGES_DEST'] = 'static/uploads/'
geolocator = Nominatim(user_agent='app')


@app.route('/')
def user_home():
    return render_template('loginevents.html')


@app.route('/AdminDashboard')
def admin_home():
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template('contactUs.html')


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
                                           create_event_form.date.data, create_event_form.location.data,'Active', 'Active', today)
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
                                              create_offline_form.date.data, create_offline_form.location.data, create_offline_form.pax.data,
                                              location.latitude, location.longitude, 'Active', 'Active', today)
        offline_dict[offline.get_event_id()] = offline
        db['Offline'] = offline_dict

        db.close()

        return redirect(url_for('retrieve_events'))
    return render_template('createOfflineEvent.html', form=create_offline_form)


@app.route('/retrieveEvents')
def retrieve_events():
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

    return render_template('retrieveEvents.html', count=len(online_list) , count1=len(offline_list), online_list=online_list, offline_list=offline_list)


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
        online.set_event_status(update_event_form.event_status.data)
        online.set_reg_status(update_event_form.reg_status.data)
        online.set_image(update_event_form.image.data.filename)

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
        update_event_form.event_status.data = online.get_event_status()
        update_event_form.reg_status.data = online.get_reg_status()
        update_event_form.image.data = online.get_image()

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
        update_offline_form.pax.data = offline.get_pax()
        update_offline_form.location.data = offline.get_location()
        update_offline_form.event_status.data = offline.get_event_status()
        update_offline_form.reg_status.data = offline.get_reg_status()
        update_offline_form.image.data = offline.get_image()

        return render_template('updateOfflineEvent.html', form=update_offline_form, offline=offline)


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

