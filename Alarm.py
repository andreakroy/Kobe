import requests
from datetime import datetime
from flask import jsonify 

'''
define an alarm object:
    title: the title of the alarm
    time: the time of the alarm
'''

class Alarm:
    def __init__(self, time, title):
        self.title = title
        if not isinstance(time, datetime):
            raise ValueError('time parameter must be a datetime object')
        self.time = time

    def __eq__(self, other):
        if not isinstance(other, Alarm):
            return False
        if other.title != self.title:
            return False
        if other.time != self.time:
            return False
        return True
    
    def get_json_dict(self):
        return {
                "time": self.time,
                "title": self.title,
            }

    def get_json(self):
        return jsonify(self.get_json_dict())

