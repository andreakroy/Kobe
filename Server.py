from flask import Flask, Response, jsonify, request, abort
from flask_restful import Resource, Api, reqparse
import requests 
import Notification as n
import Alarm as a
import datetime as d
import Reminder as r
import atexit
import json

app = Flask(__name__)
api = Api(app)


#notification class holds all notification objects on the server
#only one Notifications class can ever be instantiated to prevent confusion
class Notifications:
    '''
    Notifications is initialized with a notification list if a notifications.data file exists
    else empty list
    '''
    def __init__(self):
        try:
            with open('notifications.json', 'r') as notifications:
                temp = []
                for i in json.load(notifications):
                    try:
                        temp.append(r.Reminder.fromjson(i))
                    except:
                        temp.append(r.Reminder.fromjson(i))
                self.notification_list = temp
        except (FileNotFoundError, TypeError):
            self.notification_list = []

    
    '''
    GET Request method to return a list of Notifications from the server
        -if no type_in parameter is passed, every notification object is returned as a list of json strings
        -if type_in == Reminder, return all reminders on the server as a list of json strings
        -if type_in == Alarm, return all alarms on the server as a list of json strings
        -else if no parameter is passed, default returns all notifications
        -also can search for events with **alert time** within a range
        -if no start is provided, any notification before the end time is returned
        -if no end is provided, any notification after the start time is returned
        -if no end or start is provided, all notifications are returned
        -also searches by a query string searching the titles or the Notifcations (and the message if type is Reminder)
    '''
    def get(self, type_=n.Notification, start=None, end=None, query=None):
        if not isinstance(type_, type):
            raise TypeError('The type_parameter is invalid. type_ must be type object')
        if type_ != n.Notification and type_ != r.Reminder and type_ != a.Alarm:
            raise ValueError('The type_ parameter is invalid. type_ must be Notification, Reminder, or Alarm')
        if start != None and not isinstance(start, d.datetime):
            raise TypeError('The start parameter is invalid. start must be a datetime object')
        if end != None and not isinstance(end, d.datetime):
            raise TypeError('The end parameter is invalid. end must be a datetime object')
        if query != None and not isinstance(query, str):
            raise TypeError('The query parameter is invalid. query must be a string')
        ret = []
        for notification in self.notification_list:
            if isinstance(notification, type_):
                if start == None or notification.time >= start:
                    if end == None or notification.time <= end:
                        if query == None or query in notification.title or (type_ == r.Reminder and query in notification.msg):
                            ret.append(notification.__str__())  
        return ret

    
    def post(self, type_, time, title, start=None, end=None, msg=None):
        
        if not isinstance(type_, type):
            raise TypeError('The type_parameter is invalid. type_ must be type object')
        if type_ == a.Alarm and (start != None or end != None or msg != None):
            raise ValueError('alarm types do not have start, end, or msg parameters')
        if type_ != type_ != r.Reminder or type_ != a.Alarm:
            raise ValueError('The type_ parameter is invalid. type_ must be Reminder, or Alarm')
        if time != None and not isinstance(time, d.datetime):
            raise TypeError('The time parameter is invalid. time must be a datetime object')
        if title != None and not isinstance(title, str):
            raise TypeError('The title parameter is invalid. title must be a string')
        if start != None and not isinstance(start, d.datetime):
            raise TypeError('The start parameter is invalid. start must be a datetime object')
        if end != None and not isinstance(end, d.datetime):
            raise TypeError('The end parameter is invalid. end must be a datetime object')
        if msg != None and not isinstance(query, str):
            raise TypeError('The msg parameter is invalid. msg must be a string')
        
        if type_ == r.Reminder:
            temp = r.Reminder(time, title, start, end, msg)
            if temp not in self.notification_list:
                self.notification_list.append(temp)
                return temp
            else:
                raise ValueError('This Notification already exists on the server')
        
        elif type_ == a.Alarm:
            temp = a.Alarm(time, title)
            if temp not in self.notification_list:
                self.notification_list.append(temp)
                return temp
            else:
                raise ValueError('This Notification already exists on the server')

    def delete(self, notification):
        if not isinstance(notification, n.Notification):
            raise TypeError('notification must be a notification object')
        if notification in self.notification_list:
            temp = notification
            self.notification_list.remove(notification)
            return temp
               
context = Notifications()

#define url routing
@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    #GET
    '''
    if a title argument is passed get the notification with that title if it exists
    else get a json with every notification on the server
    '''
    if request.method == 'GET':
        try:
            try:
                if request.args['type'] == str(a.Alarm):
                    type_ = a.Alarm
                elif request.args['type'] == str(r.Reminder):
                    type_ = r.Reminder
                elif request.args['type'] == str(n.Notification):
                    type_ = n.Notification
            except KeyError as e:
                type_ = n.Notification

            try:
                start  = d.datetime.fromtimestamp(int(float(request.args['start'])))
            except KeyError as e:
                start  = None
                
            try:
                end  = d.datetime.fromtimestamp(int(float(request.args['end']))) 
            except KeyError as e:
                end = None

            try:
                query  = request.args['query']
            except KeyError as e:
                query = None

            temp = context.get(type_, start, end, query)
            if len(temp) == 0:
                return ('No Notifications found', 404)
            else:
                return jsonify(temp)
            
        except (TypeError, ValueError) as e:
            return (str(e), 400)
 
               
    #POST
    elif request.method == 'POST':
        try:
            try:
                if request.args['type'] == str(a.Alarm):
                    type_ = a.Alarm
                elif request.args['type'] == str(r.Reminder):
                    type_ = r.Reminder
                else:
                    return (str(ValueError('POST request requires a type parameter of either Alarm or Reminder')))
            
            except KeyError as e:
                return (str(ValueError('POST request requires the type of the notification')), 400)
                
            try:
                time  = d.datetime.fromtimestamp(int(float(request.args['time'])))
            except KeyError as e:
                raise ValueError('POST request requires the alert time of the notification' )
               
            try:
                title = request.args['title']
            except KeyError as e:
                raise ValueError('POST request requires the title of the notifcation')
                
            try:
                start  = d.datetime.fromtimestamp(int(float(request.args['start'])))
            except KeyError as e:
                start  = None
                
            try:
                end  = d.datetime.fromtimestamp(int(float(request.args['end']))) 
            except KeyError as e:
                end = None

            try:
                msg  = request.args['msg']
            except KeyError as e:
                msg = None
            
            return (context.post(type_, time, title, start, end, msg).__str__(), 200)
            
        except (TypeError, ValueError, OSError, OverflowError) as e:
            return (str(e), 400)

    #DELETE
    elif request.method == 'DELETE':
        try:
            if 'notification' in request.args:
                temp = n.Notification.fromjson(request.args['notification'])
                context.delete(temp)
            else:
                raise ValueError('invalid notification parameter')

        except (KeyError, TypeError, ValueError) as e:
            return (str(e), 400)



#define url routing
@app.route('/time', methods=['GET'])
def time():
    #GET
    if request.method == 'GET':
        return (str(d.datetime.now()), 200)
    else:
        return ('time only has a GET endpoint', 400)

#DRIVER            
if __name__ == '__main__':     
    app.run(debug=True)
    
