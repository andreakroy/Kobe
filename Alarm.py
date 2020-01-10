import requests
from datetime import datetime
from flask import jsonify 

'''
define an alarm object:
    title: the title of the alarm
    time: the time of the alarm
'''

class Alarm:
    def __init__(self, title, time):
        self.title = title
        self.time = time
    
    def get_json_dict(self):
        return {
                "title": self.title,
                "time": self.time,
            }

    def get_json(self):
        return jsonify(self.get_json_dict())

