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





'''
GET Request method for an individual reminder
Takes a title and returns the notification objectif it exists
Otherwise throws a ValueError
'''
def reminder_get(title):
    for notification in notification_list:
        if notification.title == title:
            return notification
    raise ValueError(title + " does not exist on the server.")


'''
GET request method for an individual alarm
Takes a time and returns the alarm object if it exists
Otherwise throws a ValueError
'''
def alarm_get(time):
    for alarm in alarm_list:
        if alarm.time == time:
            return alarm
        else:
            raise ValueError('There is no alarm at ' + time.isoformat('-') + ' on the server.')



'''
POST Request method
Takes all the requirements to create a new reminder object and appends the created reminder to notification_list
Otherwise throws a ValueError
'''
def reminder_post(title, msg, start, end):
    new = Notification.Notification(title, msg, start, end)
    print(reminder_is_unique(new))
    if reminder_is_unique(new) == -1:
        notification_list.append(new)
        return new
    else:
        raise ValueError("This event already exists")



'''
POST Request method
Takes all the requirements to create a new alarm object and appends the created alarm to alarm_list
time is passed as a datetime object
Otherwise throws a ValueError
'''
def alarm_post(time, title):
    new = a.Alarm(time, title)
    if alarm_is_unique(new) == -1:
        alarm_list.append(new)
        return new
    else:
        raise ValueError("This alarm already exists")



'''
PUT Request method
Takes a title parameter and all other notifcation parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the notifcation with that title
'''
def reminder_put(title, msg, start, end):
    #find the event on the server and update each field with the new parameters
    try:
        update = reminder_get(title)
        if msg != None:
            update.msg = msg
        if start != None:
            update.start = start
        if end != None:
            update.end = end
        return update
    except ValueError:
        raise ValueError('No event with the title ' + title + ' exists on the server.')


'''
PUT Request method
Takes a time parameter and all other alarm parameters are optional
Each parameter which isn't passed remains the same on the server
If the parameter is passed, the field is updated to the parameter
Updates the alarm at that time
'''
def alarm_put(time, title=None):
    #if the reminder is not unique throw exception
    if alarm_is_unique(a.Alarm(time, title)) != -1:
        raise ValueError("This alarm already exists")
    #find the alarm on the server and update each field with the new parameters
    for alarm in alarm_list:
        if time == alarm.time:
            if title != None:
                alarm.title = title
            return alarm
    new = a.Alarm(time, title)   
    alarm_list.append(new)
    return new




'''
DELETE Request method
Takes a reminder and removes it from the server
If the hashed value isn't found on the server, raise an exception
'''
def reminder_delete(title, msg, start, end):
    other = Notification.Notification(title, msg, start, end)
    test = reminder_is_unique(other)
    if test < 0:
        raise ValueError("The object to be deleted is not on the server")
    else:
        ret = notification_list[i]
        del notification_list[i]
        return ret


'''
DELETE Request method
Takes a title and time and removes the object with those properties from the server if it exists
If the alarm isn't found on the server, raise an exception
'''
def alarm_delete(time, title):
    other = a.Alarm(time, title)
    test = alarm_is_unique(other)
    if test < 0:
        raise ValueError("The alarm to be deleted is not on the server")
    else:
        ret = alarm_list[test]
        del alarm_list[test]
        return ret
   

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
    Method to determine whether or not the same object already exists in the list
        -if the notification does exist on the server, return the index of the object on the server
        -else return -1
    '''
    def is_unique(self, notification):
        if not isinstance(notification, n.Notification):
            raise TypeError('Notification parameter must be a notification object')
        for i in range(0, len(self.notification_list)):
            if notification == self.notification_list[i]:
                return i
        return -1

    
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
        if type_ != type_ != r.Reminder or type_ != a.Alarm:
            raise ValueError('The type_ parameter is invalid. type_ must be Reminder, or Alarm')
        if start != None and not isinstance(start, d.datetime):
            raise TypeError('The start parameter is invalid. start must be a datetime object')
        if end != None and not isinstance(end, d.datetime):
            raise TypeError('The end parameter is invalid. end must be a datetime object')
        if msg != None and not isinstance(query, str):
            raise TypeError('The msg parameter is invalid. msg must be a string')
        if type_ == r.Reminder:
            try:
                temp = r.Reminder(time, title, start, end, msg)
                if self.is_unique(temp) == -1:
                    self.notification_list.append(temp)
                    return temp
                else:
                    raise ValueError('This Notification already exists on the server')
            except (TypeError, ValueError) as e:
                pass
        else:
            try:
                temp = a.Alarm(time, title)
                if self.is_unique(temp) == -1:
                    self.notification_list.append(temp)
                    return temp
                else:
                    raise ValueError('This Notifcation already exists on the server')
            except (TypeError, ValueError) as e:
                pass

    
    
            
    ''' 
    #PUT
    elif request.method == 'PUT':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        par = {}
        if 'msg' in request.args:
            par['msg'] = request.args['msg']
        else:
            par['msg'] = None
        #if start and end times are present change them to datetimes and add to parameter list
        if 'start' in request.args:
            par['start'] = d.datetime.fromtimestamp((float(request.args['start'])))
        else:
            par['start'] = None
        if 'end' in request.args:
            par['end'] = d.datetime.fromtimestamp((float(request.args['end'])))
        else:
            par['end'] = None
        try:
            return reminder_put(request.args['title'], par['msg'], par['start'], par['end']).get_json()
        except ValueError as e:
            return (str(e), 404)
        except (OverflowError, OSError) as e:
            return (str(e) + ' (start or end parameter is not a valid unix timestamp)', 400)
 
    #DELETE
    elif request.method =='DELETE':
        if 'title' not in request.args:
            raise TypeError("No title argument was passed")
        elif 'msg' not in request.args:
            raise TypeError("No message argument was passed")
        elif 'start' not in request.args:
            raise TypeError("No start time argument was passed")
        elif 'msg' not in request.args:
            raise TypeError("No end time argument was passed")
        try:
            return reminder_delete(request.args['title'], d.datetime.fromtimestamp(float(request.args['time']))).get_json()
        except (OverflowError, OSError) as e:
            return (str(e) + ' (start or end parameter is not a valid unix timestamp)', 400)
        except ValueError as e:
        return (str(e), 404)

    
    actions to take when the server shuts down
    the notification list is exported to a binary stream called notifications.data
    this file is imported when the server restarts
    
    def on_shutdown(self):
        with open('notifications.data', 'wb') as inp:
            pickle.dump(self.notification_list, inp)



'''



context = Notifications()

#define url routing
@app.route('/notifications', methods=['GET', 'POST', 'PUT', 'DELETE'])
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
            
        except (ValueError, OSError, OverflowError) as e:
            return (str(e), 400)



#define url routing
@app.route('/time', methods=['GET'])
def time():
    #GET
    if request.method == 'GET':
        return (str(d.datetime.now()), 200)
    
#DRIVER            
if __name__ == '__main__':     
    app.run(debug=True)
    
