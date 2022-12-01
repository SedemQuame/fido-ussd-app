"""
A class to represent a USSD API and accompanying dashboard.
"""

import os
import pprint
from datetime import datetime
from session_manager import SessionManager
from menu import Menu
from flask import Flask, make_response, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ussd.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)
session = SessionManager()
menu = Menu(session)
GLOBAL_RESPONSE = ""


class Clients(db.Model):
    """DB Client Model"""
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(50))  # user input
    phone = db.Column(db.String(15))  # user input or from ussd_session
    email = db.Column(db.String(100))  # user input
    pin = db.Column(db.String(6))  # user input
    balance = db.Column(db.String(6))  # user input
    creation_date = db.Column(db.String(10))  # progam generated


class Logs(db.Model):
    """DB Logs Model"""
    id = db.Column('log_id', db.Integer, primary_key=True)
    timestamp = db.Column(db.String(50))
    phone = db.Column(db.String(15))  # user input or from ussd_session
    request_type = db.Column(db.String(15))


with app.app_context():
    db.create_all()


@app.route('/', methods=['POST', 'GET'])
def index():
    """Dummy root page"""
    GLOBAL_RESPONSE = make_response("END connection ok")
    GLOBAL_RESPONSE.headers['Content-Type'] = "text/plain"
    return GLOBAL_RESPONSE


def sanitize(phone_number):
    """Helper function that sanitizes phone numbers in international format."""
    if '233' in phone_number:
        if phone_number.index('233') == 0 or phone_number.index('+233') == 0:
            phone_number = phone_number.replace('233', '0').replace('+', '')
    return phone_number


@app.route('/new', methods=['GET', 'POST'])
def new():
    """Form handler for creating new clients"""
    # check if pin is alphanumberic contains numbers and letters.
    # check if pin has length of 4
    if request.method == 'POST':
        print()
        if len(request.form['pin']) != 4:
            flash('Account PIN must be of length 4.')
            return redirect(url_for('new'))

        # if not (request.form['pin']).isalpha():
        #     flash('Account PIN must be alpha numeric.')
        #     return redirect(url_for('new'))

        pprint.pprint(request.form)
        client = Clients(
            name=request.form['name'],
            phone=sanitize(
                request.form['phone']),
            email=request.form['email_address'],
            balance="0.0",
            pin=request.form['pin'],
            creation_date=datetime.now().strftime('%d/%m/%y %H:%M:%S.%f'))
        db.session.add(client)
        db.session.commit()
        flash('Record was successfully added')
    return render_template('new.html')


@app.route('/new-log', methods=['GET', 'POST'])
def new_log():
    """Form handler for creating new clients"""
    # check if pin is alphanumberic contains numbers and letters.
    # check if pin has length greater than or equal to 6
    if request.method == 'POST':

        log = Logs(
            timestamp=datetime.now().strftime('%d/%m/%y %H:%M:%S.%f'),
            phone=sanitize(request.form['phone']),
            request_type="Request Callback")

        db.session.add(log)
        db.session.commit()
        flash('Record was successfully added')
    return render_template('new_log.html')


@ app.route('/delete', methods=['POST'])
def delete():
    """Allows the admin to delete user datae by id."""
    if request.method == 'POST':
        if not request.form['id']:
            flash('Please enter all the fields', 'error')
        else:
            Clients.query.filter_by(id=request.form['id']).delete()
            db.session.commit()
            return redirect(url_for('show_all'))


@ app.route('/all')
def show_all():
    """Simple admin page, that shows all register clients."""
    return render_template('show_all.html', clients=Clients.query.all())


@ app.route('/logs')
def show_logs():
    """Page, that shows all requested callbacks."""
    return render_template('show_logs.html', logs=Logs.query.all())


@ app.route('/ussd/callback', methods=['POST', 'GET'])
def ussd_callback():
    """USSD callback function, called when trying to access the from USSD channel."""

    # global GLOBAL_RESPONSE

    _id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", '')

    print(_id, service_code, phone_number, text)

    if text == '':
        return menu.home(_id)
    # ----------------------------------------
    if text == '1':
        return menu.generate_otp()
    # ----------------------------------------
    if text[0] == '2' or '2*' == text[0:2]:
        return menu.check_balance_sequence(text, _id, Clients, phone_number)
    # ----------------------------------------
    if text[0] == '3':
        return menu.request_callback_sequence(text, Logs, db, phone_number)
    # ----------------------------------------
    # return menu.unavailable()
    return "END"


# creating application port.
if __name__ == '__main__':
    # run application on localhost, using port stored as PORT in env variables.
    db.create_all()
    app.run(host="0.0.0.0", port=os.environ.get('PORT'), debug=True)
