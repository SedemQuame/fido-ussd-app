import os
import json
from flask import make_response
import redis


class SessionManager:
    def __init__(self):
        if os.environ.get("REDIS_URL") != None:
            self.r = redis.from_url(os.environ.get("REDIS_URL"))
        else:
            self.r = redis.StrictRedis(decode_responses=True)
        self.id_list = []

    def checker(self, id):
        # checks to see if the session has already been saved or not.
        # returns true or false, if successful
        if (id in self.id_list) and (self.r.exists(id)):
            return True
        else:
            return False

    def save(self, id, current_form=''):
        # save the session id.
        # returns true if successful.
        self.id_list.append(id)
        return self.r.set(id, current_form)

    def set_and_expire_keys(self, id, random_otp):
        id_otp = f"{id}_otp"
        self.r.set(id_otp, random_otp)
        # otp expires after, 2mins
        self.r.expire(id_otp, 120)

    def update_id_key(self, id, response):
        # responds saves the user's menu navigation.
        old = self.r.get(id)
        new = old + response
        return self.r.set(id, new)

    def read_value(self, id):
        return self.r.get(id)

    def delete_id(self, id):
        # deletes expired session if from redis.
        # returns true or false, if successful
        self.r.delete(id)

    def execute(self):
        raise NotImplementedError

    def ussd_proceed(self, menu_text, _id, menu_code='0'):
        # self.r.set(self.id, json.dumps(self.session))
        # self.save(_id, menu_code)
        menu_text = "CON {}".format(menu_text)
        print(menu_text)
        response = make_response(menu_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def ussd_end(self, menu_text):
        # redis.delete(self.id)
        menu_text = "END {}".format(menu_text)
        response = make_response(menu_text, 200)
        response.headers['Content-Type'] = "text/plain"
        return response

    def save_session_dict(self, key, dict):
        return self.r.set(key, dict)

    def get_session_dict(self, key):
        return self.r.get(key)
