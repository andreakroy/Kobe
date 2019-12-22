from datetime import datetime
from flask import jsonify 

'''
define a reminder object:
    title: the title of the reminder
    msg: the description of the reminder
    start: the datetime object representing the start of the event
    end: the datetime object representing the end of the event    
    rpt: constant int indicating the type of repetition
'''

class Notification:
    def __init__(self, title, msg, start, end, rpt):
        self.title = title
        self.msg = msg
        self.start = start
        self.end = end
        self.rpt = rpt
    
    def get_json_dict(self):
        return {
                "title": self.title,
                "msg": self.msg,
                "start": self.start,
                "end": self.end,
                "rpt": self.rpt
            }

    def get_json(self):
        return jsonify(self.get_json_dict())

