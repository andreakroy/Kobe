import datetime as d
import Notification as n


'''
define an alarm object:
    -time -----> the alert time of the alarm
    -title ----> the title of the alarm
'''
class Alarm(n.Notification):
    
    def __init__(self, time, title):
        super(Alarm, self).__init__(time, title)
    
    @classmethod
    def fromjson(cls, json):
        return super().fromjson(json)
    
    def __eq__(self, other):
        if isinstance(other, Alarm) and super(Alarm, self).__eq__(other):
            return True
        return False
    
    def __dict__(self):
        return super(Alarm, self).__dict__()

    def __str__(self):
        return super(Alarm, self).__str__()

