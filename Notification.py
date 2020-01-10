from datetime import datetime
from flask import jsonify 

'''
define a reminder object:
    title: the title of the reminder
    msg: the description of the reminder
    start: the datetime object representing the start of the event
    end: the datetime object representing the end of the event    
'''

class Notification:
    def __init__(self, title, msg, start, end):
        self.title = title
        self.msg = msg
        if not isinstance(start, datetime):
            raise ValueError('the start time must be a datetime object')
        if not isinstance(end, datetime):
            raise ValueError('the end time must be a datetime object')
        self.start = start
        self.end = end
    
    def __eq__(self, other):
        if not isinstance(other, Notification):
            return False
        if other.title != self.title:
            return False
        if other.msg != self.msg:
            return False        
        if other.start != self.start:
            return False
        if other.end != self.end:
            return False
        return True

    
    def get_json_dict(self):
        return {
                "title": self.title,
                "msg": self.msg,
                "start": self.start,
                "end": self.end,
            }

    def get_json(self):
        return jsonify(self.get_json_dict())

