import datetime as d
import Notification as n
import json

'''
define a reminder object:
    -time -----> the alert time of the reminder
    -title ----> the title of the reminder
    -msg ------> the optional description of the reminder
    -start ----> the datetime object representing the start of the reminder
    -end ------> the datetime object representing the end of the reminder
'''
class Reminder(n.Notification):
    def __init__(self, time, title, start=None, end=None, msg=None):
        super(Reminder, self).__init__(time, title)
        if start == None:
            start = time
        if end == None:
            #t = start.replace(hour=0, minute=0, second=0, microsecond=0)
            #end = d.datetime() 
            end = start + d.timedelta(days=1)
            end = end.replace(hour=0, minute=0, second=0, microsecond=0)
        if start != None and not isinstance(start, d.datetime):
            raise TypeError('the start time must be a datetime object')
        if end != None and not isinstance(end, d.datetime):
            raise TypeError('the end time must be a datetime object')
        if msg != None and not isinstance(msg, str):
            raise TypeError('the msg parameter must be a string')
        if start >= end:
            raise ValueError('the end time must occur after the start time')
        if time > end:
            raise ValueError('the alert time must be before the end time')
        self.start = start
        self.end = end
        self.msg = msg
        
    def __eq__(self, other):
        if not super(Reminder, self).__eq__(other):
            return False
        if not isinstance(other, Reminder):
            return False
        if other.start != self.start:
            return False
        if other.end != self.end:
            return False
        if other.msg != self.msg:
            return False        
        return True

    
    def __dict__(self):
        result = super(Reminder, self).__dict__() 
        result['start'] = d.datetime.timestamp(self.start)
        result['end'] = d.datetime.timestamp(self.end)
        result['msg'] = self.msg
        return result
                

    def __str__(self):
        mod = json.loads(super(Reminder, self).__str__())
        mod['start'] = str(d.datetime.fromtimestamp(mod['start']))
        mod['end'] = str(d.datetime.fromtimestamp(mod['end']))
        return json.dumps(mod)

print(Reminder(d.datetime.now(), 'abc'))
