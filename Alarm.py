import datetime as d
import Notification as n


'''
define an alarm object:
    title: the title of the alarm
    time: the time of the alarm
'''

class Alarm(n.Notification):
    
    def __init_(self, time, title):
        super(time, title)

    def __eq__(self, other):
        if isinstance(other, Alarm) and super(Alarm, self).__eq__(other):
            return True
        return False
    
    def __dict__(self):
        return super(Alarm, self).__dict__()

    def __str__(self):
        return super(Alarm, self).__str__()

x = Alarm(d.datetime(2020, 1, 15), 'abc')
#print(x == Alarm(d.datetime(2020, 1, 15), 'abc'))
#print(dict(x))
print(x.__dict__())
print(x)
