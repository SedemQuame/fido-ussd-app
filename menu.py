"""
A class to represent a USSD menu.

    Methods
    -------
    info(additional=""):
        Prints the person's name and age.

    random_otp_generator(self):
        Generate random OTP value

    home(self, _id):
        serves the home menu

    generate_otp(self):
        Generates and sends and OTP to the user's session

    mail_random_string_to_(self, sender, receiver, password, intent, phone_number):
        Function for sending emails

    check_balance_sequence(self, text, _id, clients, db, sender_phone_number):
        USSD sequence to allow client's check their account's balance.

    request_callback_sequence(
            self,
            menu_text,
            logs,
            _db,
            sender_phone_number):
        USSD sequence to allow user's request a callback.

    unavailable(self):
        USSD sequence used when the requested service does not exist.
"""


import string
import random
import os
from datetime import datetime
from twilio.rest import Client

# global
GLOBAL_SENDER = "sedem.amekpewu.3@gmail.com"
GLOBAL_PASSWORD = "__"


class Menu():
    """Class that represents the USSD application"""
    # class attributes

    def __init__(self, session):
        self.session = session

    # --------------------------------------------------------------

    def random_otp_generator(self):
        """Generate random OTP value"""

        str_len = 4
        ran = ''.join(
            random.choices(
                # string.ascii_uppercase +
                string.digits,
                k=str_len))
        return str(ran)

    # --------------------------------------------------------------

    def home(self, _id):
        """serves the home menu"""
        phase_str = 'Main Menu \n'
        phase_str += '1. Get OTP\n'
        phase_str += '2. Check Balance\n'
        phase_str += '3. Request for a callback\n'
        return self.session.ussd_proceed(phase_str, _id, '1')

    # --------------------------------------------------------------

    def generate_otp(self):
        """Generates and sends and OTP to the user's session"""
        generated_otp = self.random_otp_generator()
        phase_str = "Generate OTP \n"
        phase_str += f"Please your generated otp is: {generated_otp}\n"
        return self.session.ussd_end(phase_str)

    # --------------------------------------------------------------

    def send_sms(self, phone_number, intent):
        """Function for sending sms, using Twilio Trial API."""
        sms_content = f"""
        \n
        FIDO CREDIT USSD
        \n
        You are receiving this SMS because you {intent},\n
        """

        account_sid = os.environ['TWILIO_ACCOUNT_SID']
        auth_token = os.environ['TWILIO_AUTH_TOKEN']
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=sms_content,
            from_='+19498280706',
            to=phone_number
        )

        print(message.sid)

    def check_balance_sequence(self, text, _id, clients, phone_number):
        """USSD sequence to allow client's check their account's balance."""
        phase_str = ''
        sender_account = clients.query.filter_by(
            phone=phone_number).all()

        if len(text.split('*')) == 1:
            phase_str += "Check Balance\n"
            phase_str += "Please enter your client id.\n"
            return self.session.ussd_proceed(phase_str, _id, '')

        if len(text.split('*')) == 2:
            input_id = text.split('*')[1]  # this input is the user's input_id
            print(f"Input id: {input_id}")
            if len(sender_account) > 0:
                print(f"Send account id id: {sender_account[0].id}")

            # a valid client id must be greater than length 6
            if len(sender_account) > 0 and str(sender_account[0].id) == str(input_id):
                phase_str += "Account Balance\n"
                phase_str += f"Your current account balance is: {sender_account[0].balance}\n"
            else:
                phase_str += "Account Balance\n"
                phase_str += f"The input id {input_id} is invalid.\n"
            return self.session.ussd_end(phase_str)

        return None
    # --------------------------------------------------------------

    def request_callback_sequence(
            self,
            text,
            logs,
            _db,
            phone_number):
        """USSD sequence to allow user's request a callback."""
        phase_str = ''
        log = logs(
            phone=phone_number,
            timestamp=datetime.now().strftime('%d/%m/%y %H:%M:%S.%f'),
            request_type="Request Callback")

        _db.session.add(log)
        _db.session.commit()

        phase_str += 'Request Callback\n'
        phase_str += 'Record was successfully added\n'
        phase_str += 'You will get a callback soon.\n'
        intent = "requested a callback."

        # send sms functionality
        self.send_sms(phone_number, intent)

        return self.session.ussd_end(phase_str)
    # --------------------------------------------------------------

    def unavailable(self):
        """ USSD sequence used when the requested service does not exist."""
        text = "Service Unavailable"
        return self.session.ussd_end(text)
    # --------------------------------------------------------------
