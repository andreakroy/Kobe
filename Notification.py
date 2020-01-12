import datetime as d
import json

class Notification:
    
    '''
    Notification object constructor
        -time -----> The alert time of the notification
        -title ----> The title of the notification
    '''
    def __init__(self, time, title):
        if not isinstance(time, d.datetime):
            raise TypeError('time parameter must be a datetime object')
        if not isinstance(title, str): 
            raise TypeError('title parameter must be an str')
        self.time = time
        self.title = title

    '''
    Check if two notification objects are equal
        -The other object must also be a notification object
        -The other object's title must be equal to this notification
        -The other object's time must be equal to this notification
    '''
    def __eq__(self, other):
        if not isinstance(other, Notification):
            return False
        if other.title != self.title:
            return False
        if other.time != self.time:
            return False
        return True
    
    '''
    dictionary representation of a Notification Object
        -time -----> timestamp for datetime object
        -title ----> title string
    '''
    def __dict__(self):
        return {
                "time": d.datetime.timestamp(self.time),
                "title": self.title,
            }
    
    '''
    returns the json string representing a Notification Object
    '''
    def __str__(self):
        return json.dumps(self.__dict__())

