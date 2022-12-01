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


import smtplib
import string
import random
from datetime import datetime

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
        phase_str = 'CON Main Menu \n'
        phase_str += '1. Get OTP\n'
        phase_str += '2. Check Balance\n'
        phase_str += '3. Request for a callback\n'
        return self.session.ussd_proceed(phase_str, _id, '1')

    # --------------------------------------------------------------

    def generate_otp(self):
        """Generates and sends and OTP to the user's session"""
        generated_otp = self.random_otp_generator()
        phase_str = "Generate OTP \n"
        phase_str += f"Please you generated otp is: {generated_otp}\n"
        return self.session.ussd_end(phase_str)

    # --------------------------------------------------------------

    def mail_random_string_to_(self, sender, receiver, password, intent):
        """Function for sending emails"""
        mail_content = f"""
            You are receiving this email because there was a {intent} for you AFROUSSD account.
        """
        receiver = ", ".join(receiver)
        email_text = f"""
            From: {sender}
            To: {receiver}
            Subject: {intent}
            {mail_content}
        """

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, ", ".join(receiver), email_text)
            server.quit()
            print('Email sent!')
        except Exception as exception:
            print(exception)

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

            # a valid client id must be greater than length 6
            if str(sender_account[0].id) == str(input_id):
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
            sender_phone_number):
        """USSD sequence to allow user's request a callback."""
        phase_str = ''
        if len(text.split('*')) == 1:
            log = logs(
                phone=sender_phone_number,
                timestamp=datetime.now().strftime('%d/%m/%y %H:%M:%S.%f'),
                request_type="Request Callback")

            _db.session.add(log)
            _db.session.commit()

            phase_str += 'Request Callback\n'
            phase_str += 'Record was successfully added\n'
            phase_str += 'You will get a callback soon.\n'

            # send sms/email functionality will be implemented here.
            # self.mail_random_string_to_(sender, receiver, password, intent)

        else:
            phase_str = "Unknown input, please try again"
        return self.session.ussd_end(phase_str)
    # --------------------------------------------------------------

    def unavailable(self):
        """ USSD sequence used when the requested service does not exist."""
        text = "Service Unavailable"
        return self.session.ussd_end(text)
    # --------------------------------------------------------------
